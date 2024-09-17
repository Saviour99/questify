/* Handles the animations on the pages */
AOS.init();

const form = document.querySelector(".upload-main");
const input = document.querySelector("#file-upload");
const uploadingFile = document.querySelector(".uploading-area");
const uploadedFile = document.querySelector(".uploaded-area");

/* Handles the file upload on the pages */
form.addEventListener("click", () => {
    input.click();
});

input.onchange = ({target}) => {
    let file = target.files[0];            /* Getting the file */
    if (file) {
        let fileName = file.name;          /* Name of the file */
        if (fileName.length >= 12){
            let splitName = fileName.split(".");
            fileName = splitName[0].substring(0, 11) + "... ." + splitName[1];
        }
        uploadFile(fileName);              /* Calling uploadFile pass it as an argument */
    }
};

/* Handles the file loading on the pages */
function uploadFile(name) {
    let xhr = new XMLHttpRequest();         /* craeting a new xml object */
    xhr.upload.addEventListener("progress", ({loaded, total}) => {
        let fileLoaded = Math.floor((loaded / total) * 100) /* Getting the percentage of the file size */
        let fileTotal = Math.floor(total / 1000) /* Getting the file size in KB */
        let fileSize;
        // If file size is less than 1024 add KB else convert file size from KM to MB.
        (fileTotal < 1024) ? fileSize = fileTotal + " KB" : fileSize = (loaded / (1024 * 1024)).toFixed(2) + " MB";
        console.log(fileLoaded, fileTotal);
        
        let uploadinHTML = `<div class="row">
                                <div class="uploading-row">
                                    <i class="fa-solid fa-file-alt"></i>
                                    <div class="content">
                                        <div class="details">
                                            <span class="info">Uploading File ...</span>
                                            <span class="percent">${fileLoaded}%</span>
                                        </div>
                                        <div class="progress-bar">
                                            <div class="progress" style="width: ${fileLoaded}%"></div>
                                        </div>
                                    </div>
                                </div>
                            </div>`;

        uploadingFile.innerHTML = uploadinHTML;

        if (loaded == total){
            uploadingFile.innerHTML = "";
            let uploadedHTML = `<div class="row">
                                    <div class="content">
                                        <i class="fa-solid fa-file-alt icon1"></i>
                                        <div class="details">
                                            <span class="info">${name} - Uploaded.</span>
                                            <span class="size">${fileSize}</span>
                                        </div>
                                        <i class="fa-solid fa-check check"></i>
                                    </div>
                                </div>`;

        uploadedFile.innerHTML = uploadedHTML;
        }
    });
    xhr.open("POST", "/upload/");
    let formData = new FormData();      /* Creating a new formData object */
    formData.append('file', input.files[0]);
    xhr.send(formData);
}

/* Handle show and hide results */
function toggleResults() {
    const showResultButton = document.querySelector("#show-results-btn");
    const correctAnswers = document.getElementsByClassName('correct-answer');
    
    let isShowing = showResultButton.getAttribute('data-showing') === 'true';

    if (isShowing) {
        // Hide results
        for (let i = 0; i < correctAnswers.length; i++) {
            correctAnswers[i].style.display = 'none';
        }
        // Update the button's text and style
        showResultButton.textContent = "Show Results";
        showResultButton.classList.remove('btn-secondary');
        showResultButton.classList.add('btn-primary');
        showResultButton.setAttribute('data-showing', 'false');
    } else {
        // Show results
        for (let i = 0; i < correctAnswers.length; i++) {
            correctAnswers[i].style.display = 'block';
        }
        // Update the button's text and style
        showResultButton.textContent = "Hide Results";
        showResultButton.classList.remove('btn-primary');
        showResultButton.classList.add('btn-secondary');
        showResultButton.setAttribute('data-showing', 'true');
    }
}
