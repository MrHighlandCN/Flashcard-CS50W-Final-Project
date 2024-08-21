document.addEventListener('DOMContentLoaded', function () {
    folder_nav_handler();
    set_nav_handler();
    card_counter();
    const add_card_button = document.querySelector("#add-card-button");
    if (add_card_button) {
        add_card_button.addEventListener('click', add_card_handler);
    }
    set_delete_card_event();
    add_card_img_handler();
    flip_card_handler();
});



function folder_nav_handler() {
    const wrapper = document.querySelector(".folders");
    const prevBtn = document.querySelector(".folder-nav-prev");
    const nextBtn = document.querySelector(".folder-nav-next");

    const scrollAmount = 500; // Khoảng cách cuộn mỗi lần nhấn nút

    if (nextBtn) {
        nextBtn.addEventListener("click", function () {
            wrapper.scrollLeft += scrollAmount;
        });
    }

    if (prevBtn) {
        prevBtn.addEventListener("click", function () {
            wrapper.scrollLeft -= scrollAmount;
        });
    }

}

function set_nav_handler() {
    const wrapper = document.querySelector(".sets");
    const prevBtn = document.querySelector(".set-nav-prev");
    const nextBtn = document.querySelector(".set-nav-next");

    const scrollAmount = 500; // Khoảng cách cuộn mỗi lần nhấn nút

    if (nextBtn) {
        nextBtn.addEventListener("click", function () {
            wrapper.scrollLeft += scrollAmount;
        });
    }

    if (prevBtn) {
        prevBtn.addEventListener("click", function () {
            wrapper.scrollLeft -= scrollAmount;
        });
    }

}

function card_counter() {
    const cards = document.querySelectorAll(".create-card-container");
    cards.forEach(function (card, index) {
        const header = card.querySelector(".card-header");
        var counter = header.querySelector(".counter");
        if (counter) {
            counter.innerHTML = `${index + 1}`;
        }
    });

}

function add_card_handler() {
    const card_container = document.querySelector("#create-cards-container");
    const index = document.querySelectorAll(".create-card-container").length;
    var additional_content = `
        <div class="row create-card-container align-items-center mt-4 card-enter">
            <div class="card-header col-12 d-flex flex-row justify-content-between align-items-center">
                <div class="counter mb-3 ms-3">

                </div>
                <button type="button" class="delete-card-btn btn me-3 mb-3 text-light"><i style="color: white; font-size: 24px;" class="bi bi-trash"></i> Delete</button>
            </div>
            <div class="col-md-5 col-12">
                <input id="content-${index}" name="content[]" type="text" class="form-control" placeholder="Enter a content" required>
            </div>
    
            <div class="col-md-5 col-10">
                <input id="meaning-${index}" name="meaning[]" type="text" class="form-control" placeholder="Enter a meaning" required>
            </div>

            <div class=" col-2 mt-2">
                <div class="image-input-container ms-auto d-flex flex-row text-center">
                    <label for="card-image-input-${index}" class="image-label text-light fw-bold w-100">
                        <i class="bi bi-image d-block"></i>
                        <p>Image</p>
                    </label>
                    <div class="image-review">
                        
                    </div>
                    <input id="card-image-input-${index}" type="file" class="card-image" name="card-image[]" accept="image/*">
                    <button type="button" class="btn text-light"><i class="bi bi-trash"></i></button>
                </div>

            </div>
        </div>
    `;

    card_container.insertAdjacentHTML("beforeend", additional_content);
    set_delete_card_event();
    card_counter();
    add_card_img_handler();
}

function set_delete_card_event() {
    const delete_card_buttons = document.querySelectorAll(".delete-card-btn");
    delete_card_buttons.forEach(function (button) {
        if (button) {
            button.addEventListener('click', function () {
                if (document.querySelectorAll(".create-card-container").length > 1) {
                    card = button.closest('.create-card-container');
                    card.classList.add('card-exit');
                    card.addEventListener('animationend', function () {
                        card.remove();
                        card_counter();
                    });
                }
            });
        }
    });
}

function add_card_img_handler() {
    const imageInputs = document.querySelectorAll('.card-image');
    imageInputs.forEach(imageInput => {
        const imgLabel = imageInput.closest('.image-input-container').querySelector('.image-label');
        const removeImgBtn = imageInput.closest('.image-input-container').querySelector('.btn');
        const imgReview = imageInput.closest('.image-input-container').querySelector('.image-review');
        imageInput.addEventListener('change', function () {

            if (imageInput.files.length > 0) {
                const img = imageInput.files[0];

                if (img && img.type.startsWith('image/')) {
                    const reader = new FileReader();
                    reader.onload = function (e) {

                        imgReview.innerHTML = `<img src="${e.target.result}" alt="Image Preview" class="img-fluid">`;
                        removeImgBtn.style.display = 'block';
                        imgLabel.style.display = 'none';
                    }

                    reader.readAsDataURL(img);
                }
                else {
                    imgReview.innerHTML = '';
                    removeImgBtn.style.display = 'none';
                }


            }
        });
        if (removeImgBtn) {
            removeImgBtn.addEventListener('click', function () {
                imageInput.value = '';
                imgReview.innerHTML = '';
                removeImgBtn.style.display = 'none';
                imgLabel.style.display = 'block';
            });
        }


    });
}

function remove_set_from_folder(set_id, set_title, btn) {
    fetch(`/remove-set-from-folder/${set_id}`, {
        method: 'POST',
    })
        .then(response => {
            if (response.ok) {
                btn.closest('.set-item').remove();
                const add_container = document.querySelector('#add-set-to-folder-form');
                add_container.innerHTML += `
                        <div class="set-item d-flex flex-row my-2 p-2">
                            <input class="form-check-input me-3" type="checkbox" value="${set_id}" name="add-set[]" id="add-set-${set_id}">
                            <label class="form-check-label text-light fw-bold flex-fill" for="add-set--${set_id}">${set_title}</label>
                        </div>  
            `
            }
            else {
                alert("Failed to remove set from folder.");
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert("An error occurred while trying to remove the set.");
        });

}


async function flip_card_handler() {
    let currentIndex = 0;
    const set_id = document.querySelector('.set-page').getAttribute('data-set-id');

    try {
        const flashcards = await get_cards(set_id); // Chờ dữ liệu từ get_cards

        if (!flashcards || flashcards.length === 0) {
            console.error('No flashcards found');
            return;
        }

        const flashcard = document.getElementById("flashcard");
        const flashcardTextFront = document.getElementById("flashcard-text-front");
        const flashcardTextBack = document.getElementById("flashcard-text-back");
        const counter = document.getElementById("counter");
        const flashcardImage = document.querySelector(".flashcard-image");

        function updateFlashcard() {
            flashcardTextFront.textContent = flashcards[currentIndex].content;
            flashcardTextBack.textContent = flashcards[currentIndex].meaning;
            counter.textContent = `${currentIndex + 1}/${flashcards.length}`;


            const imageUrl = flashcards[currentIndex].image; // Giả sử `imageUrl` là trường chứa URL hình ảnh
            if (imageUrl) {
                flashcardImage.src = imageUrl;
                flashcardImage.alt = "Flashcard image"; // Cập nhật thuộc tính alt nếu cần
            } else {
                flashcardImage.src = ''; // Xóa ảnh nếu không có URL hình ảnh
                flashcardImage.alt = ''; // Xóa thuộc tính alt nếu không có ảnh
            }
        }

        document.getElementById("flashcard").addEventListener("click", function () {
            flashcard.classList.toggle("flipped");
        });

        document.getElementById("next-btn").addEventListener("click", function () {
            if (flashcards.length > 0) {
                currentIndex = (currentIndex + 1) % flashcards.length;
                if (flashcard.classList.contains("flipped")) {
                    flashcard.classList.remove("flipped");
                }

                updateFlashcard();
            }
        });

        document.getElementById("prev-btn").addEventListener("click", function () {
            if (flashcards.length > 0) {
                currentIndex = (currentIndex - 1 + flashcards.length) % flashcards.length;
                if (flashcard.classList.contains("flipped")) {
                    flashcard.classList.remove("flipped");
                }

                updateFlashcard();
            }
        });

        // Initialize the first flashcard
        updateFlashcard();
    } catch (error) {
        console.error('Error fetching or displaying cards:', error);
    }
}

function get_cards(set_id) {
    return fetch(`/get-cards/${set_id}`)
        .then(response => response.json())
        .then(cards => {
            console.log(cards); // Kiểm tra dữ liệu trả về
            return cards;
        })
        .catch(error => {
            console.error('Cannot get cards', error);
            throw error; // Ném lỗi để xử lý ở nơi gọi hàm
        });
}

