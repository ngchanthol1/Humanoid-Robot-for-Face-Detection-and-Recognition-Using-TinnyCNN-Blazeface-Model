#!/usr/bin/env python3
"""
Dataset Validator - Check data quality before training
======================================================
"""

import cv2
import numpy as np
from pathlib import Path
from collections import defaultdict

def validate_dataset(dataset_dir='dataset'):
    """Validate dataset structure and quality"""
    
    print("=" * 70)
    print("🔍 DATASET VALIDATION")
    print("=" * 70)
    print()
    
    dataset_path = Path(dataset_dir)
    
    if not dataset_path.exists():
        print(f"❌ Dataset directory not found: {dataset_dir}")
        return False
    
    # Check subdirectories
    mrdavid_dir = dataset_path / "mrdavid"
    others_dir = dataset_path / "others"
    
    issues = []
    
    # Check Mr. David
    print("📁 Checking Mr. David images...")
    if not mrdavid_dir.exists():
        print("❌ mrdavid directory not found!")
        issues.append("Missing mrdavid directory")
    else:
        david_images = []
        david_issues = defaultdict(list)
        
        for ext in ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']:
            for img_file in sorted(mrdavid_dir.glob(ext)):
                img = cv2.imread(str(img_file))
                
                if img is None:
                    david_issues['unreadable'].append(img_file.name)
                    continue
                
                h, w = img.shape[:2]
                
                # Check size
                if h < 50 or w < 50:
                    david_issues['too_small'].append(f"{img_file.name} ({w}×{h})")
                
                # Check blur
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()
                if blur_score < 50:
                    david_issues['blurry'].append(f"{img_file.name} (score: {blur_score:.1f})")
                
                # Check brightness
                brightness = np.mean(gray)
                if brightness < 40:
                    david_issues['too_dark'].append(f"{img_file.name} (brightness: {brightness:.1f})")
                elif brightness > 215:
                    david_issues['too_bright'].append(f"{img_file.name} (brightness: {brightness:.1f})")
                
                david_images.append(img_file)
        
        print(f"  ✓ Found {len(david_images)} Mr. David images")
        
        if david_issues['unreadable']:
            print(f"  ⚠️  {len(david_issues['unreadable'])} unreadable: {david_issues['unreadable'][:3]}")
        if david_issues['too_small']:
            print(f"  ⚠️  {len(david_issues['too_small'])} too small: {david_issues['too_small'][:3]}")
        if david_issues['blurry']:
            print(f"  ⚠️  {len(david_issues['blurry'])} blurry: {david_issues['blurry'][:3]}")
        if david_issues['too_dark']:
            print(f"  ⚠️  {len(david_issues['too_dark'])} too dark: {david_issues['too_dark'][:3]}")
        if david_issues['too_bright']:
            print(f"  ⚠️  {len(david_issues['too_bright'])} too bright: {david_issues['too_bright'][:3]}")
        
        if len(david_images) < 100:
            issues.append(f"Only {len(david_images)} David images (recommended: 200+)")
            print(f"  ⚠️  RECOMMENDATION: Collect more images (have {len(david_images)}, want 200+)")
    
    print()
    
    # Check Others
    print("📁 Checking Others images...")
    if not others_dir.exists():
        print("❌ others directory not found!")
        issues.append("Missing others directory")
    else:
        others_images = []
        others_issues = defaultdict(list)
        
        for ext in ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']:
            for img_file in sorted(others_dir.glob(ext)):
                img = cv2.imread(str(img_file))
                
                if img is None:
                    others_issues['unreadable'].append(img_file.name)
                    continue
                
                h, w = img.shape[:2]
                
                if h < 50 or w < 50:
                    others_issues['too_small'].append(f"{img_file.name} ({w}×{h})")
                
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()
                if blur_score < 50:
                    others_issues['blurry'].append(f"{img_file.name} (score: {blur_score:.1f})")
                
                brightness = np.mean(gray)
                if brightness < 40:
                    others_issues['too_dark'].append(f"{img_file.name} (brightness: {brightness:.1f})")
                elif brightness > 215:
                    others_issues['too_bright'].append(f"{img_file.name} (brightness: {brightness:.1f})")
                
                others_images.append(img_file)
        
        print(f"  ✓ Found {len(others_images)} Others images")
        
        if others_issues['unreadable']:
            print(f"  ⚠️  {len(others_issues['unreadable'])} unreadable: {others_issues['unreadable'][:3]}")
        if others_issues['too_small']:
            print(f"  ⚠️  {len(others_issues['too_small'])} too small: {others_issues['too_small'][:3]}")
        if others_issues['blurry']:
            print(f"  ⚠️  {len(others_issues['blurry'])} blurry: {others_issues['blurry'][:3]}")
        if others_issues['too_dark']:
            print(f"  ⚠️  {len(others_issues['too_dark'])} too dark: {others_issues['too_dark'][:3]}")
        if others_issues['too_bright']:
            print(f"  ⚠️  {len(others_issues['too_bright'])} too bright: {others_issues['too_bright'][:3]}")
        
        if len(others_images) < 100:
            issues.append(f"Only {len(others_images)} Others images (recommended: 200+)")
            print(f"  ⚠️  RECOMMENDATION: Collect more images (have {len(others_images)}, want 200+)")
    
    print()
    
    # Check balance
    if mrdavid_dir.exists() and others_dir.exists():
        david_count = len(list(mrdavid_dir.glob('*.jpg'))) + len(list(mrdavid_dir.glob('*.png')))
        others_count = len(list(others_dir.glob('*.jpg'))) + len(list(others_dir.glob('*.png')))
        
        if david_count > 0 and others_count > 0:
            ratio = david_count / (david_count + others_count)
            
            print("📊 Dataset Balance:")
            print(f"  Mr. David: {david_count} ({ratio*100:.1f}%)")
            print(f"  Others: {others_count} ({(1-ratio)*100:.1f}%)")
            
            if ratio < 0.3 or ratio > 0.7:
                issues.append(f"Imbalanced dataset ({ratio*100:.1f}% David)")
                print(f"  ⚠️  IMBALANCED! (should be 40-60%)")
            else:
                print(f"  ✅ Well balanced!")
        print()
    
    # Summary
    print("=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)
    
    if len(issues) == 0:
        print("✅ Dataset looks good! Ready to train.")
        return True
    else:
        print(f"⚠️  Found {len(issues)} issue(s):")
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")
        print()
        print("Recommendation: Fix issues before training for best results")
        return False

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', default='dataset')
    args = parser.parse_args()
    
    validate_dataset(args.dataset)
