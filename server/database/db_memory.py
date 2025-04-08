code_blocks = [
    {
        "id": "1",
        "title": "Async Example",
        "initial_code": "async function fetchData() {\n  // TODO\n}",
        "solution_code": "async function fetchData() {\n  const res = await fetch('url');\n  return await res.json();\n}"
    },
    {
        "id": "2",
        "title": "Promise Chain",
        "initial_code": "fetch('url')\n  // TODO",
        "solution_code": "fetch('url')\n  .then(res => res.json())\n  .then(data => console.log(data));"
    },
    {
        "id": "3",
        "title": "Basic Loop",
        "initial_code": "for (let i = 0; i < 10; i++) {\n  // TODO\n}",
        "solution_code": "for (let i = 0; i < 10; i++) {\n  console.log(i);\n}"
    },
    {
        "id": "4",
        "title": "Arrow Function",
        "initial_code": "const sum = (a, b) => {\n  // TODO\n}",
        "solution_code": "const sum = (a, b) => {\n  return a + b;\n}"
    }
]
