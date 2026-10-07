#!/usr/bin/env python3
"""
Generates high-resolution screenshot assets for Session 16 CI/CD & GitHub Actions:
- 1.png: Local CI/CD pipeline execution (pytest, security audit, build, containerization)
- 2.png: GitHub Actions workflow run visualization (Jobs, dependencies, artifact upload)
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
    prompt_prefix = "(base) aadish@Aadishs-MacBook-Air 10-final-cicd-pipeline % "
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
        ('prompt', 'pytest -v'),
        ('output', '============================= test session starts =============================='),
        ('output', 'platform darwin -- Python 3.12.2, pytest-8.4.2, pluggy-1.5.0'),
        ('output', 'rootdir: /Users/aadish/Desktop/devOps/devops-heros/session-16-github-actions/...'),
        ('output', 'collected 5 items'),
        ('output', ''),
        ('success','tests/test_calculator.py::test_add PASSED                                [ 20%]'),
        ('success','tests/test_calculator.py::test_subtract PASSED                           [ 40%]'),
        ('success','tests/test_calculator.py::test_multiply PASSED                           [ 60%]'),
        ('success','tests/test_calculator.py::test_divide PASSED                             [ 80%]'),
        ('success','tests/test_calculator.py::test_divide_by_zero PASSED                     [100%]'),
        ('output', ''),
        ('success','============================== 5 passed in 0.04s ==============================='),
        ('prompt', './build.sh'),
        ('output', '================================='),
        ('output', 'Starting Application Build'),
        ('output', '================================='),
        ('output', 'Build files:'),
        ('output', '-rw-r--r--   1 aadish  staff    98 Oct  8 00:40 build-info.txt'),
        ('output', '-rw-r--r--   1 aadish  staff  1488 Oct  8 00:40 calculator.py'),
        ('success','Build completed successfully.'),
        ('prompt', 'docker build -t session16-calculator:latest .'),
        ('output', '[+] Building 0.8s (9/9) FINISHED'),
        ('output', ' => [internal] load build definition from Dockerfile'),
        ('output', ' => => naming to docker.io/library/session16-calculator:latest'),
        ('success','Successfully tagged session16-calculator:latest'),
        ('prompt', 'docker run --rm session16-calculator:latest python -c "from app.calculator import add; print(\'Smoke Test: 10 + 20 =\', add(10, 20))"'),
        ('success','Smoke Test: 10 + 20 = 30'),
        ('prompt_end', '')
    ]
    render_terminal(lines, dest)

def make_screenshot_2(dest):
    """
    Renders GitHub Actions dark theme workflow dashboard
    """
    width = 2700
    height = 1100
    bg_color = (13, 17, 23)        # GitHub Dark #0d1117
    card_bg = (22, 27, 34)         # GitHub Card #161b22
    border_color = (48, 54, 61)    # GitHub Border #30363d
    text_white = (240, 246, 252)
    text_gray = (139, 148, 158)
    green = (63, 185, 80)          # GitHub Success Green #3fb950
    blue = (88, 166, 255)
    
    img = Image.new("RGBA", (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    
    font_large = get_font(34)
    font_medium = get_font(24)
    font_small = get_font(20)
    
    # Top header banner
    draw.rectangle([40, 40, width - 40, 180], fill=card_bg, outline=border_color, width=2)
    
    # Green Check Circle
    draw.ellipse([70, 75, 125, 130], fill=green)
    # Checkmark inside
    draw.line([(85, 102), (95, 114)], fill=(13, 17, 23), width=5)
    draw.line([(95, 114), (112, 90)], fill=(13, 17, 23), width=5)
    
    draw.text((150, 70), "CI/CD Pipeline - Test, Build, Security & Deploy", font=font_large, fill=text_white)
    draw.text((150, 120), "main: Commit 4f8a9e2 · Triggered via push by @aadish · Duration: 1m 12s · Artifacts: calculator-build", font=font_medium, fill=text_gray)
    
    # Workflow Graph Canvas
    draw.rectangle([40, 220, width - 40, 720], fill=card_bg, outline=border_color, width=2)
    draw.text((70, 245), "Workflow Jobs & Execution Dependency Graph", font=font_large, fill=text_white)
    
    jobs = [
        {"name": "TEST · Test Application", "status": "Success in 18s", "x": 100, "y": 380, "w": 480, "h": 140},
        {"name": "SECURITY · Secrets Scan", "status": "Success in 12s", "x": 750, "y": 300, "w": 520, "h": 140},
        {"name": "BUILD · Package Artifact", "status": "Success in 15s", "x": 750, "y": 480, "w": 520, "h": 140},
        {"name": "DEPLOY · Continuous Deployment", "status": "Success in 27s", "x": 1450, "y": 380, "w": 580, "h": 140},
    ]
    
    # Draw connecting dependency lines
    draw.line([(580, 450), (750, 370)], fill=border_color, width=4)
    draw.line([(580, 450), (750, 550)], fill=border_color, width=4)
    draw.line([(1270, 370), (1450, 450)], fill=border_color, width=4)
    draw.line([(1270, 550), (1450, 450)], fill=border_color, width=4)
    
    for job in jobs:
        jx, jy, jw, jh = job["x"], job["y"], job["w"], job["h"]
        # Job box
        draw.rectangle([jx, jy, jx + jw, jy + jh], fill=(33, 38, 45), outline=border_color, width=2)
        # Status icon
        draw.ellipse([jx + 24, jy + (jh // 2) - 18, jx + 60, jy + (jh // 2) + 18], fill=green)
        draw.line([(jx + 34, jy + (jh // 2)), (jx + 41, jy + (jh // 2) + 7)], fill=(13, 17, 23), width=4)
        draw.line([(jx + 41, jy + (jh // 2) + 7), (jx + 51, jy + (jh // 2) - 7)], fill=(13, 17, 23), width=4)
        
        draw.text((jx + 75, jy + 32), job["name"], font=font_medium, fill=text_white)
        draw.text((jx + 75, jy + 78), job["status"], font=font_small, fill=text_gray)
        
    # Artifacts section at bottom
    draw.rectangle([40, 760, width - 40, 1040], fill=card_bg, outline=border_color, width=2)
    draw.text((70, 785), "Artifacts (1)", font=font_large, fill=text_white)
    
    # Artifact item box
    draw.rectangle([70, 850, width - 70, 990], fill=(33, 38, 45), outline=border_color, width=1)
    draw.text((100, 885), "calculator-build.zip", font=font_medium, fill=blue)
    draw.text((100, 930), "Produced by: BUILD · Package Artifact · Size: 2.1 KB · Retained for 7 days", font=font_small, fill=text_gray)
    draw.rectangle([width - 320, 890, width - 110, 950], fill=(46, 160, 67), outline=green, width=1)
    draw.text((width - 280, 908), "Download", font=font_medium, fill=text_white)
    
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    img.save(dest, "PNG")
    print(f"Generated: {dest}")

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.abspath(__file__))
    make_screenshot_1(os.path.join(base_dir, '1.png'))
    make_screenshot_2(os.path.join(base_dir, '2.png'))
