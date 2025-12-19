import { test, expect } from "@playwright/test";

test("admin can trigger salary import", async ({ page }) => {
  await page.addInitScript(() => {
    localStorage.setItem("token", "test-token");
    localStorage.setItem("role", "admin");
  });

  await page.route("**/admin/import/salary", (route) =>
    route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({ status: "ok" }),
    })
  );

  await page.goto("http://localhost:5173");

  await expect(page).toHaveURL(/\/admin/);

  await page.getByRole("button", { name: "Gehalt (Salary)" }).click();

  await expect(
    page.getByText("✔ Erfolgreich importiert")
  ).toBeVisible({ timeout: 6000 });
});

test("user sees dashboard with loaded charts (mocked)", async ({ page }) => {

  await page.addInitScript(() => {
    localStorage.setItem("token", "test-user-token");
    localStorage.setItem("role", "user");
  });

  await page.route("**/statistics/**", (route) => {
    route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify([
        { name: "Test", value: 10 }
      ]),
    });
  });

  await page.goto("http://localhost:5173");

  await expect(page).toHaveURL(/\/dashboard/);
  await expect(page.getByText("Willkommen!")).toBeVisible();
});
