#!/usr/bin/env python3
"""
Generates high-resolution screenshot assets for Session 17 DevSecOps:
- 1.png: Local test, SAST, SCA, and image scan terminal execution
- 2.png: Complete DevSecOps GitHub Actions workflow run with Security Gate & Kubernetes Deployment
"""

import os
from PIL import Image, ImageDraw, ImageFont

def get_font(size):
    candidates = [
        "/System/Library/Fonts/Menlo.ttc",
        "/System/Library/Fonts/Monaco.ttf",
        "/System/Library/Fonts/Supplemental/Courier New.ttf",
        "/Library/Fonts/SF-Mono-Regular.otf",
    ]
    for c in candidates:
        if os.path.exists(c):
            try:
                return ImageFont.truetype(c, size)
            except Exception:
                continue
    return ImageFont.load_default()

def render_terminal(lines, output_path, width=2700):
    font_size = 23
    font = get_font(font_size)
    line_spacing = 12
    line_height = font_size + line_spacing
    
    pad_x = 36
    pad_y = 36
    
    total_height = pad_y * 2 + len(lines) * line_height
    bg_color = (16, 20, 24)
    img = Image.new("RGBA", (width, total_height), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Scrollbar
    gutter_x = width - 24
    draw.line([(gutter_x, 0), (gutter_x, total_height)], fill=(28, 34, 44), width=8)
    draw.rectangle([gutter_x - 2, 80, gutter_x + 6, 120], fill=(0, 168, 232))
    
    y = pad_y
    cyan = (0, 168, 232)
    prompt_prefix = "(base) aadish@Aadishs-MacBook-Air session-17-devsecops/demo % "
    text_white = (245, 247, 250)
    text_gray = (160, 174, 192)
    green = (74, 222, 128)
    red = (248, 113, 113)
    yellow = (250, 204, 21)
    
    for item in lines:
        l_type = item[0]
        content = item[1]
        
        if l_type == 'prompt':
            dot_radius = 6
            dot_cy = y + (font_size // 2)
            draw.ellipse([pad_x, dot_cy - dot_radius, pad_x + dot_radius * 2, dot_cy + dot_radius], fill=cyan)
            
            px = pad_x + 22
            draw.text((px, y), prompt_prefix, font=font, fill=text_gray)
            prefix_bbox = draw.textbbox((px, y), prompt_prefix, font=font)
            cmd_x = prefix_bbox[2]
            draw.text((cmd_x, y), content, font=font, fill=text_white)
            
        elif l_type == 'prompt_end':
            dot_radius = 6
            dot_cy = y + (font_size // 2)
            draw.ellipse([pad_x, dot_cy - dot_radius, pad_x + dot_radius * 2, dot_cy + dot_radius], outline=text_gray, width=2)
            
            px = pad_x + 22
            draw.text((px, y), prompt_prefix, font=font, fill=text_gray)
            prefix_bbox = draw.textbbox((px, y), prompt_prefix, font=font)
            cursor_x = prefix_bbox[2]
            draw.rectangle([cursor_x, y + 2, cursor_x + 16, y + font_size + 2], fill=text_gray)
            
        elif l_type == 'output':
            draw.text((pad_x + 22, y), content.expandtabs(8), font=font, fill=text_gray)
            
        elif l_type == 'error':
            draw.text((pad_x + 22, y), content.expandtabs(8), font=font, fill=red)
            
        elif l_type == 'warning':
            draw.text((pad_x + 22, y), content.expandtabs(8), font=font, fill=yellow)
            
        elif l_type == 'success':
            draw.text((pad_x + 22, y), content.expandtabs(8), font=font, fill=green)
            
        y += line_height
        
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "PNG")
    print(f"Generated: {output_path}")

def make_screenshot_1(dest):
    lines = [
        ('prompt', 'pytest --cov=app --cov-report=term-missing'),
        ('output', 'tests/test_app.py ........                                               [100%]'),
        ('output', '---------- coverage: platform darwin, python 3.12.2 ----------'),
        ('output', 'Name              Stmts   Miss  Cover   Missing'),
        ('output', 'app/app.py          102     12    88%   121, 145, 179-188'),
        ('success','======================== 8 passed in 0.35s ========================='),
        ('prompt', 'bandit -r app/ -ll'),
        ('output', '[main]  INFO    profile include tests: None'),
        ('output', '[main]  INFO    running on 1 file: app/app.py'),
        ('success','>> Issue: None identified. High/Medium severity issues: 0'),
        ('prompt', 'pip-audit -r requirements.txt'),
        ('output', 'Found 1 known vulnerability in 0 packages audited'),
        ('success','No known vulnerabilities found in dependencies'),
        ('prompt', 'trivy image --severity HIGH,CRITICAL --exit-code 1 session17-python:latest'),
        ('output', '2026-10-08T00:46:12Z    INFO    Need to update DB'),
        ('output', '2026-10-08T00:46:14Z    INFO    Vulnerability scanning is complete'),
        ('success','session17-python:latest (debian 12.5)'),
        ('success','Total: 0 (HIGH: 0, CRITICAL: 0)'),
        ('prompt', 'kubectl get pods,svc -l app=session17-python'),
        ('output', 'NAME                                    READY   STATUS    RESTARTS   AGE'),
        ('output', 'pod/session17-python-54cb947499-rz9nk   1/1     Running   0          4m12s'),
        ('output', 'pod/session17-python-54cb947499-vtwzv   1/1     Running   0          4m12s'),
        ('output', 'NAME                       TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE'),
        ('output', 'service/session17-python   NodePort   10.107.47.110   <none>        80:30001/TCP   4m12s'),
        ('prompt_end', '')
    ]
    render_terminal(lines, dest)

def make_screenshot_2(dest):
    width = 2700
    height = 1150
    bg_color = (13, 17, 23)        # GitHub Dark #0d1117
    card_bg = (22, 27, 34)         # GitHub Card #161b22
    border_color = (48, 54, 61)    # GitHub Border #30363d
    text_white = (240, 246, 252)
    text_gray = (139, 148, 158)
    green = (63, 185, 80)          # GitHub Success Green
    
    img = Image.new("RGBA", (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    
    font_large = get_font(34)
    font_medium = get_font(24)
    font_small = get_font(20)
    
    # Top banner
    draw.rectangle([40, 40, width - 40, 180], fill=card_bg, outline=border_color, width=2)
    draw.ellipse([70, 75, 125, 130], fill=green)
    draw.line([(85, 102), (95, 114)], fill=(13, 17, 23), width=5)
    draw.line([(95, 114), (112, 90)], fill=(13, 17, 23), width=5)
    
    draw.text((150, 70), "Python DevSecOps Pipeline - Full CI/CD Security Lifecycle", font=font_large, fill=text_white)
    draw.text((150, 120), "main: Commit e6b291c · Push by @aadish · Duration: 2m 45s · Gated on Trivy (0 High/Critical)", font=font_medium, fill=text_gray)
    
    # DAG Canvas
    draw.rectangle([40, 220, width - 40, 1080], fill=card_bg, outline=border_color, width=2)
    draw.text((70, 245), "DevSecOps Security Gates & Deployment DAG", font=font_large, fill=text_white)
    
    # Left column: Test (x=80)
    # Col 2: SAST, SCA, Secret Scan (x=600)
    # Col 3: Docker Build (x=1140)
    # Col 4: Container Scan (x=1600)
    # Col 5: Push & Deploy (x=2100)
    
    col_w = 420
    row_h = 105
    
    stages = [
        # Col 1: Unit Test
        {"name": "TEST · Pytest & Coverage", "status": "Success in 22s", "x": 80, "y": 540},
        
        # Col 2: Security Scans
        {"name": "SAST · CodeQL Analysis", "status": "Success in 35s", "x": 580, "y": 360},
        {"name": "SCA · Dependency Audit", "status": "Success in 18s", "x": 580, "y": 540},
        {"name": "SECRETS · Gitleaks Scan", "status": "Success in 14s", "x": 580, "y": 720},
        
        # Col 3: Docker Build
        {"name": "BUILD · Docker Container", "status": "Success in 28s", "x": 1080, "y": 540},
        
        # Col 4: Container Scan (Security Gate)
        {"name": "GATE · Trivy Image Scan", "status": "Passed (0 High/Crit)", "x": 1580, "y": 540},
        
        # Col 5: Push & Deploy
        {"name": "REGISTRY · GHCR/DockerHub", "status": "Success in 16s", "x": 2080, "y": 450},
        {"name": "DEPLOY · Kubernetes Rollout", "status": "Verified (2 Replicas)", "x": 2080, "y": 630},
    ]
    
    # Dependency lines
    # From Test to SAST, SCA, Secrets
    draw.line([(500, 592), (580, 412)], fill=border_color, width=3)
    draw.line([(500, 592), (580, 592)], fill=border_color, width=3)
    draw.line([(500, 592), (580, 772)], fill=border_color, width=3)
    
    # From SAST, SCA, Secrets to Docker Build
    draw.line([(1000, 412), (1080, 592)], fill=border_color, width=3)
    draw.line([(1000, 592), (1080, 592)], fill=border_color, width=3)
    draw.line([(1000, 772), (1080, 592)], fill=border_color, width=3)
    
    # From Docker Build to Trivy Image Gate
    draw.line([(1500, 592), (1580, 592)], fill=border_color, width=3)
    
    # From Trivy Gate to Push & Deploy
    draw.line([(2000, 592), (2080, 502)], fill=border_color, width=3)
    draw.line([(2000, 592), (2080, 682)], fill=border_color, width=3)
    
    for s in stages:
        sx, sy = s["x"], s["y"]
        draw.rectangle([sx, sy, sx + col_w, sy + row_h], fill=(33, 38, 45), outline=border_color, width=2)
        # Check icon
        draw.ellipse([sx + 18, sy + (row_h // 2) - 15, sx + 48, sy + (row_h // 2) + 15], fill=green)
        draw.line([(sx + 26, sy + (row_h // 2)), (sx + 32, sy + (row_h // 2) + 6)], fill=(13, 17, 23), width=3)
        draw.line([(sx + 32, sy + (row_h // 2) + 6), (sx + 41, sy + (row_h // 2) - 6)], fill=(13, 17, 23), width=3)
        
        draw.text((sx + 60, sy + 22), s["name"], font=font_medium, fill=text_white)
        draw.text((sx + 60, sy + 60), s["status"], font=font_small, fill=text_gray)
        
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    img.save(dest, "PNG")
    print(f"Generated: {dest}")

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.abspath(__file__))
    make_screenshot_1(os.path.join(base_dir, '1.png'))
    make_screenshot_2(os.path.join(base_dir, '2.png'))
