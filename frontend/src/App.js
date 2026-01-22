import React, { useState } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState("");

  const uploadFile = async () => {
    const formData = new FormData();
    formData.append("file", file);

    const res = await axios.post("http://127.0.0.1:5000/upload", formData);
    setResult(res.data.result);
  };

  return (
    <div>
      <h1>Deepfake Detection System</h1>
      <input type="file" onChange={(e)=>setFile(e.target.files[0])} />
      <button onClick={uploadFile}>Check</button>
      <h2>Result: {result}</h2>
    </div>
  );
}

export default App;
