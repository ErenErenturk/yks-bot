// frontend/src/App.jsx
import React, { useState } from "react";
import { predictTopic, extractText, sendFeedback } from "./api";

function App() {
  const [question, setQuestion] = useState("");
  const [predictedTopic, setPredictedTopic] = useState(null);
  // eslint-disable-next-line no-unused-vars
  const [file, setFile] = useState(null);
  const [feedbackSent, setFeedbackSent] = useState(false);

  const handlePredict = async () => {
    const res = await predictTopic(question);
    if (res.topic) {
      setPredictedTopic(res.topic);
      setFeedbackSent(false);
    }
  };

  const handleImageUpload = async (e) => {
    const file = e.target.files[0];
    setFile(file);
    const res = await extractText(file);
    if (res.text) {
      setQuestion(res.text);
    }
  };

  const handleFeedback = async (isCorrect) => {
    if (!predictedTopic || !question) return;
    await sendFeedback({ question, topic: predictedTopic, is_correct: isCorrect });
    setFeedbackSent(true);
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif", maxWidth: "700px", margin: "auto" }}>
      <h1>YKS Soru Konu Tahmini</h1>
      <p>Bir soru yazın veya görsel yükleyin. Sistem konuyu tahmin etsin.</p>

      <textarea
        rows="4"
        style={{ width: "100%", padding: "10px" }}
        placeholder="Soruyu buraya yazın..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />

      <div style={{ margin: "1rem 0" }}>
        <input type="file" accept="image/*" onChange={handleImageUpload} />
      </div>

      <button onClick={handlePredict} style={{ padding: "10px 20px" }}>
        Tahmin Et
      </button>

      {predictedTopic && (
        <div style={{ marginTop: "1.5rem" }}>
          <h3>Tahmin Edilen Konu: {predictedTopic}</h3>
          {!feedbackSent ? (
            <>
              <p>Bu tahmin doğru mu?</p>
              <button onClick={() => handleFeedback(true)} style={{ marginRight: "10px" }}>
                Evet
              </button>
              <button onClick={() => handleFeedback(false)}>Hayır</button>
            </>
          ) : (
            <p>Geri bildiriminiz için teşekkürler!</p>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
