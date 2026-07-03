const form = document.getElementById("predictForm");

const loading = document.getElementById("loading");
const result = document.getElementById("result");

const prediction = document.getElementById("prediction");
const confidence = document.getElementById("confidence");
const message = document.getElementById("message");

form.addEventListener("submit", async function (e) {

    e.preventDefault();

    loading.style.display = "block";
    result.style.display = "none";

    const data = {

        age: document.getElementById("age").value,
        sex: document.getElementById("sex").value,
        cp: document.getElementById("cp").value,
        trestbps: document.getElementById("trestbps").value,
        chol: document.getElementById("chol").value,
        fbs: document.getElementById("fbs").value,
        restecg: document.getElementById("restecg").value,
        thalach: document.getElementById("thalach").value,
        exang: document.getElementById("exang").value,
        oldpeak: document.getElementById("oldpeak").value,
        slope: document.getElementById("slope").value,
        ca: document.getElementById("ca").value,
        thal: document.getElementById("thal").value

    };

    try {

        const response = await fetch("/predict", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(data)

        });

        const ans = await response.json();

        loading.style.display = "none";
        result.style.display = "block";

        prediction.innerHTML = ans.emoji + " " + ans.prediction;

        confidence.innerHTML = "Confidence : " + ans.confidence + "%";

        message.innerHTML = ans.message;

        result.classList.remove("low-risk");
        result.classList.remove("high-risk");

        if (ans.color === "green") {

            result.classList.add("low-risk");

        }
        else {

            result.classList.add("high-risk");

        }

    }

    catch (error) {

        loading.style.display = "none";

        alert("Server Error!");

        console.log(error);

    }

});