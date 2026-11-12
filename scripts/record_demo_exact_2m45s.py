import asyncio
import os
import shutil
import time
from pathlib import Path
from playwright.async_api import async_playwright

async def record_exact_2m45s_demo():
    output_dir = Path(r"c:\Users\Srishanth S\Desktop\Sri folder\PayPal AI Hackathon\demo_recording")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    temp_dir = output_dir / "temp_video_exact_2m45s"
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir(parents=True, exist_ok=True)

    print("==================================================================")
    print("🎬 STARTING EXACT 2:45 (165.0s) MASTER DEMO RECORDING")
    print("==================================================================")
    
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

        start_time = time.time()

        async def sync_wait_until(target_seconds, label=""):
            elapsed = time.time() - start_time
            remaining = target_seconds - elapsed
            if remaining > 0:
                print(f"[{time.strftime('%M:%S', time.gmtime(elapsed))}] {label} -> holding for {remaining:.1f}s until {time.strftime('%M:%S', time.gmtime(target_seconds))}...")
                await page.wait_for_timeout(int(remaining * 1000))
            else:
                print(f"[{time.strftime('%M:%S', time.gmtime(elapsed))}] {label} -> passed target by {-remaining:.1f}s")

        async def pause(seconds):
            await page.wait_for_timeout(int(seconds * 1000))

        # ------------------------------------------------------------------
        # SCENE 1: Opening Dashboard (0:00 – 0:20) [20s target]
        # ------------------------------------------------------------------
        print("[0:00] SCENE 1: Opening Dashboard & Architecture Badges...")
        await page.goto("http://localhost:8000")
        await page.wait_for_load_state("networkidle")
        await pause(3)

        # Highlight Top Ribbon & PayPal status
        await page.mouse.move(960, 25)
        await pause(2)
        await page.mouse.move(1430, 70)
        await pause(2)

        # Smooth scrolling down across all 4 milestone cards
        await page.mouse.wheel(0, 380)
        await pause(3)
        await page.mouse.wheel(0, 380)
        await pause(3)
        await page.mouse.wheel(0, -760)
        await sync_wait_until(20.0, "End Scene 1 (0:20)")

        # ------------------------------------------------------------------
        # SCENE 2: Create New Milestone & Specifications (0:20 – 0:45) [25s target]
        # ------------------------------------------------------------------
        print("[0:20] SCENE 2: Creating Milestone with Specifications...")
        create_btn = page.locator("button:has-text('+ New Milestone')").first
        if await create_btn.is_visible():
            await create_btn.hover()
            await pause(1.5)
            await create_btn.click()
            await pause(3)

            # Select Agentic AI Data Bounty template
            template_btn = page.locator("button:has-text('Agentic AI Data Bounty')").first
            if await template_btn.is_visible():
                await template_btn.hover()
                await pause(1.5)
                await template_btn.click()
                await pause(3)
            else:
                hvac_btn = page.locator("button:has-text('HVAC Capacitor')").first
                if await hvac_btn.is_visible():
                    await hvac_btn.click()
                    await pause(3)

            # Scroll inside modal to highlight AI specifications checklist
            await page.mouse.wheel(0, 250)
            await pause(4)
            await page.mouse.wheel(0, -250)
            await pause(2)

            # Submit milestone creation
            submit_create = page.locator("button:has-text('Create Escrow Milestone')").first
            if await submit_create.is_visible():
                await submit_create.hover()
                await pause(1.5)
                await submit_create.click()
        
        await sync_wait_until(45.0, "End Scene 2 (0:45)")

        # ------------------------------------------------------------------
        # SCENE 3: PayPal Authorization Hold (0:45 – 1:05) [20s target]
        # ------------------------------------------------------------------
        print("[0:45] SCENE 3: Demonstrating PayPal Orders v2 Authorization Hold...")
        lock_btn = page.locator("button:has-text('Lock Escrow')").first
        if await lock_btn.is_visible():
            await lock_btn.hover()
            await pause(2)
            await lock_btn.click()
            await pause(6)

            # Close PayPal modal cleanly
            close_paypal = page.locator("button:has(svg.lucide-x)").first
            if await close_paypal.is_visible():
                await close_paypal.click()
        
        await sync_wait_until(65.0, "End Scene 3 (1:05)")

        # ------------------------------------------------------------------
        # SCENE 4: Switch to Contractor View (1:05 – 1:15) [10s target]
        # ------------------------------------------------------------------
        print("[1:05] SCENE 4: Switching to Contractor & AI Scanner Tab...")
        contractor_tab = page.locator("button:has-text('Contractor & AI Scanner'), button:has-text('AI Scanner')").first
        await contractor_tab.hover()
        await pause(1.5)
        await contractor_tab.click()
        await pause(3)

        # Select the HVAC milestone
        milestone_select = page.locator("select").first
        if await milestone_select.is_visible():
            try:
                await milestone_select.select_option(value="ms-hvac-7701")
            except Exception:
                pass
        
        await sync_wait_until(75.0, "End Scene 4 (1:15)")

        # ------------------------------------------------------------------
        # SCENE 5: Submit GOOD Proof & AI PASS (Auto-Capture) (1:15 – 1:50) [35s target]
        # ------------------------------------------------------------------
        print("[1:15] SCENE 5: Submitting Compliant Deliverable (PASS -> Confetti -> Auto-Capture)...")
        pass_sample = page.locator("button:has-text('Compliant')").first
        if await pass_sample.is_visible():
            await pass_sample.hover()
            await pause(2.5)
            await pass_sample.click()
            await pause(4)

            # Trigger AI Scan
            submit_scan_btn = page.locator("button:has-text('Submit Proof & Trigger AI Scan')").first
            if await submit_scan_btn.is_visible():
                await submit_scan_btn.hover()
                await pause(2)
                await submit_scan_btn.click()
                # Watch live scanning animation, criteria turning green, confetti explosion!
                await pause(12)
        
        await sync_wait_until(110.0, "End Scene 5 (1:50)")

        # ------------------------------------------------------------------
        # SCENE 6: AI Verdict Details (1:50 – 2:00) [10s target]
        # ------------------------------------------------------------------
        print("[1:50] SCENE 6: Reviewing Detailed AI Verdict & Criteria Evidence...")
        await page.mouse.wheel(0, 380)
        await pause(4)
        await page.mouse.wheel(0, -380)
        await sync_wait_until(120.0, "End Scene 6 (2:00)")

        # ------------------------------------------------------------------
        # SCENE 7: Submit BAD Proof & AI FAIL → Auto-VOID (2:00 – 2:20) [20s target]
        # ------------------------------------------------------------------
        print("[2:00] SCENE 7: Submitting Deficient Deliverable (FAIL -> Auto-VOID)...")
        # Select the Industrial Chiller milestone
        if await milestone_select.is_visible():
            try:
                await milestone_select.select_option(value="ms-refrig-8805")
                await pause(2)
            except Exception:
                pass

        # Select the Deficient sample
        fail_sample = page.locator("button:has-text('Violation'), button:has-text('Deficient')").first
        if await fail_sample.is_visible():
            await fail_sample.hover()
            await pause(2)
            await fail_sample.click()
            await pause(3)

            # Trigger AI Scan on deficient deliverable
            submit_scan_btn2 = page.locator("button:has-text('Submit Proof & Trigger AI Scan')").first
            if await submit_scan_btn2.is_visible():
                await submit_scan_btn2.hover()
                await pause(1.5)
                await submit_scan_btn2.click()
                await pause(7)
        
        await sync_wait_until(140.0, "End Scene 7 (2:20)")

        # ------------------------------------------------------------------
        # SCENE 8: Cryptographic Proof Ledger (2:20 – 2:32) [12s target]
        # ------------------------------------------------------------------
        print("[2:20] SCENE 8: Inspecting SHA-256 Proof Ledger & Dual Blocks...")
        ledger_tab = page.locator("button:has-text('Proof Ledger'), button:has-text('Ledger')").first
        await ledger_tab.hover()
        await pause(1.5)
        await ledger_tab.click()
        await pause(3)

        # Highlight verified badge
        await page.mouse.move(750, 160)
        await pause(2)

        # Scroll through SHA-256 blocks showing BOTH captured & voided records
        await page.mouse.wheel(0, 450)
        await pause(2.5)
        await page.mouse.wheel(0, -450)
        await sync_wait_until(152.0, "End Scene 8 (2:32)")

        # ------------------------------------------------------------------
        # SCENE 9: Dispute Defense Pack (2:32 – 2:40) [8s target]
        # ------------------------------------------------------------------
        print("[2:32] SCENE 9: Dispute Defense Pack Modal & PDF Export...")
        client_tab = page.locator("button:has-text('Client Escrow'), button:has-text('Client')").first
        await client_tab.click()
        await pause(1.5)

        dispute_btn = page.locator("button:has-text('Dispute Pack')").first
        if await dispute_btn.is_visible():
            await dispute_btn.hover()
            await pause(1)
            await dispute_btn.click()
            await pause(3)

            # Hover over Download PDF button
            pdf_btn = page.locator("button:has-text('Download Official PDF'), a:has-text('Download PDF'), button:has-text('Download PDF')").first
            if await pdf_btn.is_visible():
                await pdf_btn.hover()
                await pause(1.5)

            # Close modal cleanly
            await page.keyboard.press("Escape")
            await pause(0.5)
            close_btn = page.locator("button:has(svg.lucide-x)").first
            if await close_btn.is_visible():
                await close_btn.click()

        await sync_wait_until(160.0, "End Scene 9 (2:40)")

        # ------------------------------------------------------------------
        # SCENE 10: Human Override & Closing View (2:40 – 2:45) [5s target]
        # ------------------------------------------------------------------
        print("[2:40] SCENE 10: Human Override & Platform Closing View...")
        manual_btn = page.locator("button:has-text('Manual Release'), button:has-text('Manual Void')").first
        if await manual_btn.is_visible():
            await manual_btn.hover()
            await pause(2)

        await page.mouse.move(960, 25)
        await sync_wait_until(165.0, "Exact Finish at 165.0s (2:45)")

        print("==================================================================")
        print("🎬 EXACT 165.0 SECONDS REACHED. CLOSING BROWSER FOR ENCODING...")
        print("==================================================================")
        await page.close()
        await context.close()
        await browser.close()

    recorded_files = list(temp_dir.glob("*.webm"))
    if recorded_files:
        raw_video = recorded_files[0]
        final_mp4 = output_dir / "proofledger_demo_exact_2m45s.mp4"
        print(f"Recorded raw video to: {raw_video}")
        print("Encoding final exact 2:45 1080p MP4...")
        ffmpeg_cmd = f'ffmpeg -y -i "{raw_video}" -c:v libx264 -pix_fmt yuv420p -r 30 "{final_mp4}"'
        os.system(ffmpeg_cmd)
        print(f"SUCCESS! Master demo video saved to: {final_mp4}")
    else:
        print("No video file captured.")

if __name__ == "__main__":
    asyncio.run(record_exact_2m45s_demo())
