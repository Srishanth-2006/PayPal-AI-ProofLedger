import asyncio
import os
import shutil
from pathlib import Path
from playwright.async_api import async_playwright

async def record_demo():
    output_dir = Path(r"c:\Users\Srishanth S\Desktop\Sri folder\PayPal AI Hackathon\demo_recording")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Clean previous temp videos
    temp_dir = output_dir / "temp_video"
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir(parents=True, exist_ok=True)

    print("Launching Playwright with video recording...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=["--start-maximized", "--disable-infobars"]
        )
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            record_video_dir=str(temp_dir),
            record_video_size={"width": 1920, "height": 1080}
        )
        page = await context.new_page()

        # Helper for human-like pauses
        async def pause(seconds):
            await page.wait_for_timeout(seconds * 1000)

        print("[Scene 1] Navigating to Dashboard...")
        await page.goto("http://localhost:8000")
        await page.wait_for_load_state("networkidle")
        await pause(4)

        # Smooth scroll down to showcase milestones
        print("[Scene 1] Scrolling across milestones...")
        await page.mouse.wheel(0, 400)
        await pause(3)
        await page.mouse.wheel(0, 400)
        await pause(3)
        await page.mouse.wheel(0, -800)
        await pause(2)

        # Scene 2: Open Create Milestone Modal
        print("[Scene 2] Opening Create Milestone Modal...")
        create_btn = page.locator("button:has-text('+ New Milestone')").first
        if await create_btn.is_visible():
            await create_btn.click()
            await pause(3)

            # Click a template
            hvac_template = page.locator("button:has-text('HVAC Capacitor & Calibration')").first
            if await hvac_template.is_visible():
                await hvac_template.click()
                await pause(3)
            
            # Submit creation
            submit_create = page.locator("button:has-text('Create Escrow Milestone')").first
            if await submit_create.is_visible():
                await submit_create.click()
                await pause(3)

        # Scene 3: Switch to Contractor & AI Scanner
        print("[Scene 3] Switching to Contractor & AI Scanner Tab...")
        contractor_tab = page.locator("button:has-text('Contractor & AI Scanner'), button:has-text('AI Scanner')").first
        await contractor_tab.click()
        await pause(3)

        # Scene 4: Select Compliant Sample (Pass case)
        print("[Scene 4] Selecting Compliant Deliverable Proof...")
        pass_sample = page.locator("button:has-text('Compliant')").first
        if await pass_sample.is_visible():
            await pass_sample.click()
            await pause(3)

            print("[Scene 5] Submitting Proof & Triggering Autonomous AI Scanner...")
            submit_scan_btn = page.locator("button:has-text('Submit Proof & Trigger AI Scan')").first
            if await submit_scan_btn.is_visible():
                await submit_scan_btn.click()
                # Watch scanning animation, criteria scoring, and confetti
                await pause(8)

        # Scroll down to examine AI criteria checklist and confidence score
        print("[Scene 6] Reviewing AI Criteria Checklist & Scores...")
        await page.mouse.wheel(0, 450)
        await pause(4)
        await page.mouse.wheel(0, -450)
        await pause(2)

        # Scene 7: Proof Ledger Tab
        print("[Scene 7] Switching to Proof Ledger...")
        ledger_tab = page.locator("button:has-text('Proof Ledger'), button:has-text('Ledger')").first
        await ledger_tab.click()
        await pause(4)

        # Scroll down through cryptographic blocks
        print("[Scene 7] Inspecting SHA-256 blocks...")
        await page.mouse.wheel(0, 500)
        await pause(3)
        await page.mouse.wheel(0, 500)
        await pause(3)
        await page.mouse.wheel(0, -1000)
        await pause(2)

        # Scene 8: Dispute Pack Modal
        print("[Scene 8] Opening Dispute Defense Pack...")
        client_tab = page.locator("button:has-text('Client Escrow'), button:has-text('Client')").first
        await client_tab.click()
        await pause(2)

        dispute_btn = page.locator("button:has-text('Dispute Pack')").first
        if await dispute_btn.is_visible():
            await dispute_btn.click()
            await pause(4)
            # Close via the 'X' button in header or Escape key
            await page.keyboard.press("Escape")
            await pause(1)
            # In case Escape doesn't close, click the close button with SVG icon
            close_btn = page.locator("button:has(svg.lucide-x)").first
            if await close_btn.is_visible():
                await close_btn.click()
                await pause(1)

        # Scene 9: Webhook Simulator
        print("[Scene 9] Webhook Simulator...")
        webhook_tab = page.locator("button:has-text('Webhook Simulator'), button:has-text('Webhooks')").first
        await webhook_tab.click()
        await pause(3)

        # Scene 10: Final Dashboard view
        await client_tab.click()
        await pause(3)

        print("Finished script walkthrough. Closing page to finalize video recording...")
        await page.close()
        await context.close()
        await browser.close()

    # Find recorded webm and convert to mp4 with ffmpeg
    recorded_files = list(temp_dir.glob("*.webm"))
    if recorded_files:
        raw_video = recorded_files[0]
        final_mp4 = output_dir / "proofledger_demo_walkthrough.mp4"
        print(f"Recorded raw video to: {raw_video}")
        print("Converting to standard 1080p MP4 using FFmpeg...")
        ffmpeg_cmd = f'ffmpeg -y -i "{raw_video}" -c:v libx264 -pix_fmt yuv420p -r 30 "{final_mp4}"'
        os.system(ffmpeg_cmd)
        print(f"SUCCESS! Final polished video saved to: {final_mp4}")
    else:
        print("No video file captured.")

if __name__ == "__main__":
    asyncio.run(record_demo())
