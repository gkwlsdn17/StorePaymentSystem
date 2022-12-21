
var page = 1;
var today = new Date();
var year = today.getFullYear();
var month = (today.getMonth() + 1).toString().padStart(2,'0');
var day = today.getDate().toString().padStart(2,'0');
var start = year + '-' + month + '-01';
var end = year + '-' + month + '-' + day;
var keyword = ''

$(window).scroll(function(){
    
    if (Math.round( $(window).scrollTop()) == $(document).height() - $(window).height()) {
        page += 1;
        start = start.replaceAll('-','');
        end = end.replaceAll('-','');
        $.ajax({
            type: 'GET',
            url: '/admin/point/more?start=' + start + '&end=' + end + '&keyword=' + keyword + '&page=' + page,
            success: function (data) {
                console.log(data)
                data = JSON.parse(data)
                console.log(data)
                
                data.forEach(p => {
                    console.log(p)
                    $("#tbd").append("<tr><td>"+p.num+"</td>\
                                        <td>"+p.crtime+"</td>\
                                        <td>"+p.user_id+"</td>\
                                        <td>"+p.point+"</td>\
                                        <td>"+p.memo+"</td></tr>");
                });
                
            }
        });
    }
})
$(document).ready(function(){
    console.log(start)
    console.log(end)
    document.getElementsByName('start')[0].value = start;
    document.getElementsByName('end')[0].value = end;
});

function search(start, end, keyword){
    start = $('input[name=start]').val();
    end = $('input[name=end]').val();
    keyword = $('input[name=keyword]').val();

    start = start.replaceAll('-','');
    end = end.replaceAll('-','');
    window.location.href= '/admin/point?start=' + start + '&end=' + end + '&keyword=' + keyword
}