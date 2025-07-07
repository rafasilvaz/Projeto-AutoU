
/* Script de validação */

const textoInput = document.getElementById('textbox');
const arquivoInput = document.getElementById('filebutton');
const erroDiv = document.getElementById('erro');
const form = document.querySelector('form');

textoInput.addEventListener('input', () => {
    if (textoInput.value.trim() !== "") {
        arquivoInput.value = "";
    }
});

arquivoInput.addEventListener('change', () => {
    if (arquivoInput.files.length > 0) {
        textoInput.value = "";
    }
});

form.addEventListener('submit', (e) => {
    erroDiv.textContent = "";
    if (textoInput.value.trim() === "" && arquivoInput.files.length === 0) {
        e.preventDefault();
        erroDiv.textContent = "Você deve escrever um texto ou enviar um arquivo.";
    }
});