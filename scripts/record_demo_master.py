import asyncio
import os
import shutil
from pathlib import Path
from playwright.async_api import async_playwright

async def record_master_demo():
    output_dir = Path(r"c:\Users\Srishanth S\Desktop\Sri folder\PayPal AI Hackathon\demo_recording")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    temp_dir = output_dir / "temp_video_master"
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir(parents=True, exist_ok=True)

    print("Launching Playwright for MASTER 2:50 Demo Recording...")
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

        async def pause(seconds):
            await page.wait_for_timeout(seconds * 1000)

        # ------------------------------------------------------------------
        # SCENE 1: Introduction & Client Escrow Dashboard (0:00 - 0:20) ~20s
        # ------------------------------------------------------------------
        print("[Scene 1] Dashboard Overview & Architecture Badges...")
        await page.goto("http://localhost:8000")
        await page.wait_for_load_state("networkidle")
        await pause(4)

        # Hover over Top Ribbon and PayPal Sandbox status badge
        await page.mouse.move(960, 25)
        await pause(2)
        await page.mouse.move(1430, 70)
        await pause(2)

        # Smooth scroll to show the 4 contract milestones in different states
        print("[Scene 1] Scrolling across all milestone states...")
        await page.mouse.wheel(0, 380)
        await pause(3)
        await page.mouse.wheel(0, 380)
        await pause(3)
        await page.mouse.wheel(0, -760)
        await pause(3)

        # ------------------------------------------------------------------
        # SCENE 2: Milestone Creation & AI Specifications (0:20 - 0:42) ~22s
        # ------------------------------------------------------------------
        print("[Scene 2] Milestone Creation & Contract Specifications...")
        create_btn = page.locator("button:has-text('+ New Milestone')").first
        if await create_btn.is_visible():
            await create_btn.hover()
            await pause(1.5)
            await create_btn.click()
            await pause(3)

            # Choose the Agentic AI Data Bounty template
            bounty_template = page.locator("button:has-text('Agentic AI Data Bounty')").first
            if await bounty_template.is_visible():
                await bounty_template.hover()
                await pause(1.5)
                await bounty_template.click()
                await pause(3)
            else:
                hvac_template = page.locator("button:has-text('HVAC Capacitor & Calibration')").first
                if await hvac_template.is_visible():
                    await hvac_template.click()
                    await pause(3)

            # Scroll inside modal to highlight AI specifications checklist
            await page.mouse.wheel(0, 250)
            await pause(3)
            await page.mouse.wheel(0, -250)
            await pause(2)

            # Submit milestone creation
            submit_create = page.locator("button:has-text('Create Escrow Milestone')").first
            if await submit_create.is_visible():
                await submit_create.hover()
                await pause(1.5)
                await submit_create.click()
                await pause(5)

        # ------------------------------------------------------------------
        # SCENE 3: PayPal Authorization Hold Flow (0:42 - 0:58) ~16s
        # ------------------------------------------------------------------
        print("[Scene 3] Demonstrating PayPal Authorization Lock...")
        lock_btn = page.locator("button:has-text('Lock Escrow')").first
        if await lock_btn.is_visible():
            await lock_btn.hover()
            await pause(2)
            await lock_btn.click()
            await pause(4)

            # Close PayPal modal
            close_paypal = page.locator("button:has(svg.lucide-x)").first
            if await close_paypal.is_visible():
                await close_paypal.click()
                await pause(2)

        # ------------------------------------------------------------------
        # SCENE 4: Contractor View & AI PASS (Auto-Capture) (0:58 - 1:32) ~34s
        # ------------------------------------------------------------------
        print("[Scene 4] Contractor View - Submitting Compliant Deliverable (PASS)...")
        contractor_tab = page.locator("button:has-text('Contractor & AI Scanner'), button:has-text('AI Scanner')").first
        await contractor_tab.hover()
        await pause(1.5)
        await contractor_tab.click()
        await pause(4)

        # Select the HVAC milestone
        milestone_select = page.locator("select").first
        if await milestone_select.is_visible():
            try:
                await milestone_select.select_option(value="ms-hvac-7701")
                await pause(2)
            except Exception:
                pass

        # Select compliant sample
        pass_sample = page.locator("button:has-text('Compliant')").first
        if await pass_sample.is_visible():
            await pass_sample.hover()
            await pause(2)
            await pass_sample.click()
            await pause(4)

            # Trigger AI Scan
            submit_scan_btn = page.locator("button:has-text('Submit Proof & Trigger AI Scan')").first
            if await submit_scan_btn.is_visible():
                await submit_scan_btn.hover()
                await pause(2)
                await submit_scan_btn.click()
                # Watch live scanning animation, criteria verification & confetti auto-capture!
                await pause(10)

        # Scroll to inspect detailed criteria checklist with green checks
        await page.mouse.wheel(0, 380)
        await pause(4)
        await page.mouse.wheel(0, -380)
        await pause(2)

        # ------------------------------------------------------------------
        # SCENE 5: AI REJECTION & AUTO-VOID (1:32 - 2:05) ~33s ⭐ CRITICAL
        # ------------------------------------------------------------------
        print("[Scene 5] Submitting Deficient Deliverable (FAIL -> Auto-VOID)...")
        # Select the Industrial Chiller milestone
        if await milestone_select.is_visible():
            try:
                await milestone_select.select_option(value="ms-refrig-8805")
                await pause(3)
            except Exception:
                pass

        # Select the Deficient sample
        fail_sample = page.locator("button:has-text('Violation'), button:has-text('Deficient')").first
        if await fail_sample.is_visible():
            await fail_sample.hover()
            await pause(2)
            await fail_sample.click()
            await pause(4)

            # Trigger AI Scan on deficient proof
            if await submit_scan_btn.is_visible():
                await submit_scan_btn.hover()
                await pause(2)
                await submit_scan_btn.click()
                # Watch scanning animation detect deficiencies, score drop, and auto-void!
                await pause(9)

        # Scroll down to inspect AI failure reasoning & void notice
        await page.mouse.wheel(0, 380)
        await pause(4)
        await page.mouse.wheel(0, -380)
        await pause(2)

        # ------------------------------------------------------------------
        # SCENE 6: Human Override Controls (2:05 - 2:18) ~13s
        # ------------------------------------------------------------------
        print("[Scene 6] Human Override Controls (Responsible AI)...")
        client_tab = page.locator("button:has-text('Client Escrow'), button:has-text('Client')").first
        await client_tab.hover()
        await pause(1.5)
        await client_tab.click()
        await pause(3)

        # Hover over manual override buttons
        manual_btn = page.locator("button:has-text('Manual Release'), button:has-text('Manual Void')").first
        if await manual_btn.is_visible():
            await manual_btn.hover()
            await pause(3)

        # ------------------------------------------------------------------
        # SCENE 7: Cryptographic Proof Ledger (2:18 - 2:35) ~17s
        # ------------------------------------------------------------------
        print("[Scene 7] Proof Ledger & Cryptographic Integrity...")
        ledger_tab = page.locator("button:has-text('Proof Ledger'), button:has-text('Ledger')").first
        await ledger_tab.hover()
        await pause(1.5)
        await ledger_tab.click()
        await pause(4)

        # Highlight verified badge
        await page.mouse.move(750, 160)
        await pause(2)

        # Scroll through SHA-256 blocks showing BOTH captured & voided records
        await page.mouse.wheel(0, 500)
        await pause(4)
        await page.mouse.wheel(0, 500)
        await pause(4)
        await page.mouse.wheel(0, -1000)
        await pause(2)

        # ------------------------------------------------------------------
        # SCENE 8: Dispute Defense Pack & PDF Bundle (2:35 - 2:48) ~13s
        # ------------------------------------------------------------------
        print("[Scene 8] Dispute Defense Pack & PDF Evidence Bundle...")
        await client_tab.click()
        await pause(2)

        dispute_btn = page.locator("button:has-text('Dispute Pack')").first
        if await dispute_btn.is_visible():
            await dispute_btn.hover()
            await pause(2)
            await dispute_btn.click()
            await pause(5)

            # Hover over Download PDF button
            pdf_btn = page.locator("button:has-text('Download Official PDF'), a:has-text('Download PDF'), button:has-text('Download PDF')").first
            if await pdf_btn.is_visible():
                await pdf_btn.hover()
                await pause(2.5)

            # Close modal cleanly
            await page.keyboard.press("Escape")
            await pause(1)
            close_btn = page.locator("button:has(svg.lucide-x)").first
            if await close_btn.is_visible():
                await close_btn.click()
                await pause(1.5)

        # ------------------------------------------------------------------
        # SCENE 9: Webhook Simulator & Closing Wrap-up (2:48 - 2:54) ~6s
        # ------------------------------------------------------------------
        print("[Scene 9] Webhooks & Final Closing View...")
        webhook_tab = page.locator("button:has-text('Webhook Simulator'), button:has-text('Webhooks')").first
        await webhook_tab.hover()
        await pause(1.5)
        await webhook_tab.click()
        await pause(3)

        # Return to main dashboard for final shot
        await client_tab.click()
        await pause(3)

        print("Master recording finished! Closing browser...")
        await page.close()
        await context.close()
        await browser.close()

    recorded_files = list(temp_dir.glob("*.webm"))
    if recorded_files:
        raw_video = recorded_files[0]
        final_mp4 = output_dir / "proofledger_master_demo_complete.mp4"
        print(f"Recorded raw video to: {raw_video}")
        print("Encoding master high-definition 1080p MP4...")
        ffmpeg_cmd = f'ffmpeg -y -i "{raw_video}" -c:v libx264 -pix_fmt yuv420p -r 30 "{final_mp4}"'
        os.system(ffmpeg_cmd)
        print(f"SUCCESS! Master complete demo video saved to: {final_mp4}")
    else:
        print("No video file captured.")

if __name__ == "__main__":
    asyncio.run(record_master_demo())
