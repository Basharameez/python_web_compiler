let editor;
const defaultCode = `# Example:\nimport pandas as pd\nprint("Hello, World!")\n# Upload and read:\ndf = pd.read_csv("uploads/your_file.csv")\nprint(df.head())`;

require.config({ paths: { vs: 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.43.0/min/vs' }});
require(["vs/editor/editor.main"], function () {
  editor = monaco.editor.create(document.getElementById("editor"), {
    value: defaultCode,
    language: "python",
    theme: "vs-dark",
    automaticLayout: true,
    fontSize: 14
  });
});

async function runCode() {
  const code = editor.getValue();
  const res = await fetch("/run", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code })
  });
  const data = await res.json();
  document.getElementById("output").textContent = data.output;
  if (data.plot) {
    const img = document.getElementById("plot");
    img.src = `data:image/png;base64,${data.plot}`;
    img.style.display = "block";
  } else {
    document.getElementById("plot").style.display = "none";
  }
}

function resetCode() {
  editor.setValue(defaultCode);
}

document.getElementById("fileInput").addEventListener("change", async function () {
  const file = this.files[0];
  const formData = new FormData();
  formData.append("file", file);
  const res = await fetch("/upload", { method: "POST", body: formData });
  const data = await res.json();
  alert(data.message + "\n\nUse this path in your code:\n" + data.path);
});
