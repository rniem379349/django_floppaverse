const notifwebSocketURL = 'ws://'
+ window.location.host
+ '/ws/notifications/'

const notifSocket = new WebSocket(
    notifwebSocketURL,
    protocol = "ws",
);

const chat_notification_number_badge = document.querySelector('#chat-notification-num-badge');
const chat_notification_button = document.querySelector('#chat-notification-button');

const notification_number_badge = document.querySelector('#notification-num-badge');
const notification_button = document.querySelector('#notification-button');

let notifications_cleared = false;
let chat_notifications_cleared = false;

notifSocket.onmessage = function(e) {
    let data = JSON.parse(e.data);
    let notifications_container = document.querySelector('#notifications-container');
    let chat_notifications_container = document.querySelector('#chat-notifications-container');
    let chat_notification_for_user = user_already_in_chat_notifications(data.sender);

    let should_increment_chat_notification_badge = data.chat_notification
    && Boolean(!chat_notification_for_user)
    || chat_notifications_cleared; // if user already in notifications, don't increment

    let list_item_html = '';
    if (data.chat_notification) {
        list_item_html = `
        <li>
            <a class="dropdown-item d-flex align-items-center notification-strip" id="user_chat_notification_${data.sender}" href="/chat/private/${data.room}">
                <div class="p-1 pic-container">
                    <img class="img-thumbnail p-0 h-100 rounded-circle" src="${data.sender_pic}" alt="*">
                </div>
                <div class="p-1">
                    <small>${data.sender_username} | </small><small class="notification-timestamp">${data.sent}</small><br>
                    <small>${data.message}</small>
                </div>
            </a>
        </li>
        `;
        if (chat_notification_for_user) {
            chat_notification_for_user.innerHTML = list_item_html;
        } else {
            let nothing_new = chat_notifications_container.querySelector(".chat_notifications-nothing-new");
            if (nothing_new) {
                chat_notifications_container.innerHTML = list_item_html;
            } else {
                chat_notifications_container.innerHTML += list_item_html;
            }
        }
        // increment the chat notification count
        if (should_increment_chat_notification_badge) {
            let num_chat_notifications = chat_notification_number_badge.innerHTML;
            num_chat_notifications++;
            chat_notification_number_badge.innerText = num_chat_notifications;
            chat_notification_number_badge.classList.remove("d-none");
            chat_notifications_cleared = false;
        }
    } else {
        list_item_html = `
        <li>
            <a class="dropdown-item d-flex align-items-center notification-strip" href=${data.notification_url}>
                <div class="dropdown-item d-flex align-items-center notification-strip">
                    <div class="p-1 pic-container">
                        <img class="img-thumbnail p-0 h-100 rounded-circle" src="${data.sender_pic}" alt="*">
                    </div>
                    <div class="p-1">
                        <small>${data.sender_username} | </small><small class="notification-timestamp">${data.sent}</small><br>
                        <small>${data.message}</small>
                    </div>
                </div>
            </a>
        </li>
        `;
        let nothing_new = notifications_container.querySelector(".notifications-nothing-new");
        if (nothing_new) {
            notifications_container.innerHTML = list_item_html;
        } else {
            notifications_container.innerHTML += list_item_html;
        }
        notification_number_badge.innerText = "!";
        notification_number_badge.classList.remove("d-none");
        notifications_cleared = false;
    }
};

function user_already_in_chat_notifications(user_pk) {
    let chat_notification_container_for_user = document.querySelector(`#user_chat_notification_${user_pk}`);
    return chat_notification_container_for_user;
}

notifSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly: ', e);
};

notifSocket.onerror = function(e) {
    console.error('Chat socket encountered error: ', e);
};

if (chat_notification_button) {
    chat_notification_button.addEventListener('click', () => {
        chat_notifications_cleared = true;
        let num_chat_notifications = chat_notification_number_badge.innerHTML;
        num_chat_notifications = 0;
        chat_notification_number_badge.innerText = num_chat_notifications;
        chat_notification_number_badge.classList.add("d-none");
    })
}

if (notification_button) {
    notification_button.addEventListener('click', () => {
        notifications_cleared = true;
        notification_number_badge.innerText = "";
        notification_number_badge.classList.add("d-none");
    })
}
