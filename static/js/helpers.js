export function toastNotification(title, success=true, duration=2500, gravity="bottom", position="right", style={
    background: success ? "#16a34a" : "#dc3545",
    borderRadius: "8px",
    fontSize: "14px",
    padding: "10px 20px"
}) {

    Toastify({
        text: title,
        duration: duration,
        gravity: gravity,
        position: position,
        style: style
    }).showToast();
}