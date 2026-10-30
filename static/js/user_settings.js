document.addEventListener("DOMContentLoaded", function () {

    const photoInput = document.getElementById("profile_photo");
    const photoName = document.getElementById("selectedPhotoName");

    if (photoInput && photoName) {

        photoInput.addEventListener("change", function () {

            if (photoInput.files.length > 0) {
                const file = photoInput.files[0];

                photoName.textContent = file.name;

                if (!file.type.startsWith("image/")) {
                    alert("Please select a valid image file.");
                    photoInput.value = "";
                    photoName.textContent = "No new photo selected";
                }
            } else {
                photoName.textContent = "No new photo selected";
            }

        });

    }

});