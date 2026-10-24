$(document).ready(function () {
    $(document).on("click", ".pagination a.page-link", function (e) {
        e.preventDefault();
        var url = $(this).attr("href");
        if (url && url !== "#") {
            $("#list-block").load(url);
        }
    });
});
