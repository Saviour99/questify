AOS.init();

const form = document.querySelector("form");
const input = document.querySelector("#file-upload");
const uploadingFile = document.querySelector(".uploading-area");
const uploadedFile = document.querySelector(".uploaded-area");
const failed = document.querySelector(".failed");

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

function uploadFile(name) {
    let xhr = new XMLHttpRequest();         /* craeting a new xml object */
    xhr.open("POST", "/main.py");    /* Using the post method sends the xml object to the specified URL */
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
    let formData = new FormData(form);      /* Creating a new formData object */ 
    xhr.send(formData);                     /* Sending the formData to python backend */
}
