'use strict';

let filesData = {
    files: [],
    addFile: function(file) {
        this.files.push(file);
    },
    removeFile: function(fileName) {
        this.files = this.files.filter(file => file.name !== fileName);
    },
    fileCount: 0,
};


document.getElementById("click_choose_files").addEventListener("click", function (){
    document.getElementById("id_files").click();
})
document.querySelector('input[type="file"]').addEventListener('change', handleChange);

function handleChange(event) {
    let files = event.target.files;

    let fileNames = '';
    for (let i = 0; i < files.length; i++) {
        filesData.fileCount++;
        filesData.addFile(files[i]);
        let fileName = files[i].name;
        fileNames += '<div class="me-2 mb-1 border border-success p-1 rounded" filename="' + fileName + '">' + fileName + ' <button type="button" class="btn btn-sm btn-danger" onclick="removeFile(\'' + fileName + '\')">Удалить</button></div>';
    }

    document.getElementById('file-names').innerHTML += fileNames;

    updateStateFiles()
    updateFileCount(filesData.fileCount);
}

function removeFile(fileName) {
    filesData.removeFile(fileName);
    filesData.fileCount--;

    let fileDiv = document.querySelector('div[filename="' + fileName + '"]');
    if (fileDiv) {
        fileDiv.remove();
    }

    updateStateFiles()
    updateFileCount();
}

function updateFileCount() {
    document.getElementById('file-count').innerHTML = 'Файлов: ' + filesData.fileCount + ' шт.';
}

function updateStateFiles() {
    let dt = new DataTransfer();

    for (let i= 0; i < filesData.files.length; i++) {
        let file = filesData.files[i];
        let newFile = new File([file], file.name, { type: file.type });
        dt.items.add(newFile);
    }

    const fileList = dt.files;
    let inputElement = document.getElementById('id_files');
    inputElement.files = fileList;

    uploadFilesToServer(fileList);
}

function uploadFilesToServer(files) {
    const uploadFilesUrl = document.getElementById('upload-files-url').getAttribute('data-url');
    console.log("uploadFilesUrl 2 ", uploadFilesUrl)
    console.log("FileList : ", files);
    let formData = new FormData();
    for (let i = 0; i < files.length; i++) {
        formData.append('files[]', files[i]);
    }
    console.log(formData)
    console.log("formData.values() :", formData.values())
    $.ajax({
        url: uploadFilesUrl,
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function(data) {
            console.log(data);
            // Добавьте дополнительную обработку ответа сервера здесь, если необходимо
        },
        error: function(xhr, status, error) {
            console.error(xhr.responseText);
        }
    });
}



