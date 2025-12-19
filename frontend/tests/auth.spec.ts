import { test, expect } from "@playwright/test";

test("admin is redirected to admin dashboard after login", async ({ page }) => {
  await page.addInitScript(() => {
    localStorage.setItem("token", "test-token");
    localStorage.setItem("role", "admin");
  });

  await page.goto("http://localhost:5173");

  await expect(page).toHaveURL(/\/admin/);
  await expect(page.getByText("Adminbereich")).toBeVisible();
});
