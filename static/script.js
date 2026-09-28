const form = document.getElementById("wine-form");
const resultBox = document.getElementById("result");
const submitBtn = document.getElementById("submit-btn");

// A typical red wine row, handy for quick testing.
const SAMPLE = [7.4, 0.7, 0, 1.9, 0.076, 11, 34, 0.9978, 3.51, 0.56, 9.4];

document.getElementById("sample-btn").addEventListener("click", () => {
  [...form.elements].filter(e => e.tagName === "INPUT")
    .forEach((input, i) => { input.value = SAMPLE[i] ?? ""; });
});

function show(html, isError = false) {
  resultBox.innerHTML = html;
  resultBox.classList.toggle("error", isError);
  resultBox.classList.remove("hidden");
}

function describe(score) {
  if (score === 0) return "Not good ✋";
  if (score === 1) return "Good 🍷";
  if (score >= 7) return "Excellent 🌟";
  if (score >= 6) return "Good 🍷";
  if (score >= 5) return "Average 🙂";
  return "Poor 👎";
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  if (!form.reportValidity()) return;

  const payload = {};
  new FormData(form).forEach((v, k) => { payload[k] = v; });

  submitBtn.disabled = true;
  submitBtn.textContent = "Predicting…";
  try {
    const res = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Prediction failed");

    const conf = data.confidence != null ? `<div>Confidence: ${data.confidence}%</div>` : "";
    show(`<div class="score">${data.prediction}</div>
          <div class="label">${describe(data.prediction)}</div>${conf}`);
  } catch (err) {
    show(err.message, true);
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = "Predict quality";
  }
});
