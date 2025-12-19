import { apiFetch } from "./api";

export async function getQuestions() {
  return apiFetch("/survey/questions");
}

export async function getOptions(api: string, params: Record<string, number> = {}) {
  const query = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    query.append(key, value.toString());
  });

  const urlWithQuery = Object.keys(params).length ? `${api}?${query.toString()}` : api;

  console.log("Fetching options for", api, "with params:", params);
  console.log("Full URL:", urlWithQuery);

  return apiFetch(urlWithQuery);
}

export async function getStatistic(
  url: string,
  params: Record<string, number | string | undefined>
) {
  const query = new URLSearchParams();

  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null) {
      query.append(key, String(value));
    }
  });

  return apiFetch(`${url}?${query.toString()}`);
}

export async function getSummary(payload: any) {
  return apiFetch("/survey/summary", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}