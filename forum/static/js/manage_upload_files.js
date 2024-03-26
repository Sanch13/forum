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
    uploadFilesToServer(fileList)
    let inputElement = document.getElementById('id_files');
    inputElement.files = fileList;
}

function uploadFilesToServer(fileList) {
    let formData = new FormData();
    for (let i = 0; i < fileList.length; i++) {
        formData.append('files', fileList[i]);
    }
    return formData
    //     for (let i = 0; i < filesData.files.length; i++) {
    //     formData.append('files', filesData.files[i]);
    // }

    // $.ajax({
    //     url: "{% url 'vote:upload_files' %}",
    //     type: 'POST',
    //     data: formData,
    //     processData: false,
    //     contentType: false,
    //     success: function(data) {
    //         console.log(data);
    //         $('#upload-success').show();
    //         $('#submitBtn').prop('disabled', false); // Делаем кнопку отправки активной после успешной загрузки
    //     },
    //     error: function(xhr, status, error) {
    //         console.error(xhr.responseText);
    //     }
    // });
}
