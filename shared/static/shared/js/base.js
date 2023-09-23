document.addEventListener('DOMContentLoaded', adjustSanitiserAllowList, false);
document.addEventListener('DOMContentLoaded', initBootstrapTooltips, false);
document.addEventListener('DOMContentLoaded', initBootstrapPopovers, false);
document.addEventListener('DOMContentLoaded', initPopoverCopyToClipboardEventListeners, true);

function initBootstrapTooltips() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
      return new bootstrap.Tooltip(tooltipTriggerEl)
    })
}

function initBootstrapPopovers() {
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl, {
            container: popoverTriggerEl,
            trigger: 'focus',
            html: true,
            content: function() {
                var post_pk = popoverTriggerEl.dataset.postPk;
                var post_popover = document.querySelector(`#post-${post_pk}-popover`);
                return post_popover.innerHTML;
            }
        })
    })
}

function initPopoverCopyToClipboardEventListeners() {
    // dynamically added popovers need their event handlers dynamically bound to the popover content.
    // we use inderted.bs.popover event, which fires when the popover's inner content is rendered.
    // From there we get the 'Copy' button and bind the copy to clipboard functionality to it.
        document.querySelectorAll('[data-bs-toggle="popover"]').forEach(but => {
        but.addEventListener('inserted.bs.popover', function(popover) {
            var copyToClipboardButton = popover.target.querySelector(".btn-copy-to-clipboard");
            copyToClipboardButton.addEventListener('click', handleCopyToClipboardClick, false);
        })
    })
}

function handleCopyToClipboardClick(event) {
    var isCopyToClipboardButton = event.target.classList.contains('btn-copy-to-clipboard');
    if (isCopyToClipboardButton) {
        var inputVal = event.target.previousElementSibling.value;
        navigator.clipboard.writeText(inputVal).then(res => {
            event.target.innerText = "Copied!"
            setTimeout(() => {
                event.target.innerText = "Copy"
            }, 1000);
        })
    }
}

function adjustSanitiserAllowList() {
    // Allows certain HTML elements to be abble to use them in popovers etc.
    var myDefaultAllowList = bootstrap.Tooltip.Default.allowList
    myDefaultAllowList.input = ['type', 'class', 'placeholder', 'aria-label', 'value', 'aria-describedby', 'readonly']
    myDefaultAllowList.button = ['type']
}
