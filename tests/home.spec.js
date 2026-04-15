const { test, expect } = require("@playwright/test");

test.describe("Artemis 2 Photos landing page", () => {
  test("loads the editorial homepage with SEO metadata and gallery content", async ({
    page,
    isMobile
  }) => {
    const pageErrors = [];
    const consoleErrors = [];

    page.on("pageerror", (error) => pageErrors.push(error.message));
    page.on("console", (message) => {
      if (message.type() === "error") {
        consoleErrors.push(message.text());
      }
    });

    await page.goto("/");

    await expect(page).toHaveTitle(/Artemis 2 Photos/i);
    await expect(page.locator("h1")).toHaveText(/Artemis 2 Photos/i);
    await expect(page.locator(".hero-visual img")).toBeVisible();
    await expect(page.locator(".gallery-card")).toHaveCount(8);
    await expect(page.locator(".fact-card")).toHaveCount(3);
    await expect(page.locator("script[src='/assets/public-env.js']")).toHaveCount(1);
    await expect(page.locator("link[rel='canonical']")).toHaveAttribute(
      "href",
      "https://anapaularenault.lol/"
    );

    const faq = page.locator(".faq-item").first();
    if (isMobile) {
      await faq.locator("summary").tap();
    } else {
      await faq.locator("summary").click();
    }
    await expect.poll(async () => faq.evaluate((node) => node.hasAttribute("open"))).toBe(
      true
    );

    const iconHref = await page
      .locator("link[rel='icon'][sizes='32x32']")
      .getAttribute("href");
    expect(iconHref).toBe("/assets/brand/favicon-32.png");

    const altCount = await page.locator("img[alt]").count();
    expect(altCount).toBeGreaterThanOrEqual(10);

    const publicEnv = await page.evaluate(() => window.__ARTEMIS_PUBLIC_ENV__);
    expect(publicEnv.webUrl).toBe("https://anapaularenault.lol");
    expect(publicEnv.projectName).toBe("artemis-2-photos");
    expect(publicEnv.googleAnalyticsId).toBe("G-Y6YZ3N2BHD");
    expect(publicEnv.clarityProjectId).toBe("wbz78yq9o9");

    await expect(page.locator("html")).toHaveAttribute("data-clarity-enabled", "true");
    await expect(page.locator("html")).toHaveAttribute("data-ga-enabled", "true");
    await expect(page.locator("html")).toHaveAttribute("data-ga-measurement-id", "G-Y6YZ3N2BHD");

    expect(pageErrors).toEqual([]);
    expect(consoleErrors).toEqual([]);
  });

  test("keeps the hero and gallery legible on mobile", async ({ page, isMobile }) => {
    test.skip(!isMobile, "Mobile-specific assertions only apply on mobile.");

    await page.goto("/");

    await expect(page.locator(".site-header")).toBeVisible();
    await expect(page.locator(".hero-copy")).toBeVisible();
    await expect(page.locator(".gallery-grid")).toBeVisible();
    await expect(page.locator(".hero-actions a").first()).toBeInViewport();
    await expect(page.locator(".gallery-card").nth(1)).toBeVisible();
  });
});
