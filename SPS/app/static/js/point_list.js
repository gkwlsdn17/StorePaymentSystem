
var page = 1;
var start = ''
var end = ''
var keyword = ''

$(window).scroll(function(){
    
    if (Math.round( $(window).scrollTop()) == $(document).height() - $(window).height()) {
        page += 1;
        start = $('input[name=start]').val().replaceAll('-','');
        end = $('input[name=end]').val().replaceAll('-','');

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

function search(start, end, keyword){
    start = $('input[name=start]').val();
    end = $('input[name=end]').val();
    keyword = $('input[name=keyword]').val();

    start = start.replaceAll('-','');
    end = end.replaceAll('-','');
    window.location.href= '/admin/point?start=' + start + '&end=' + end + '&keyword=' + keyword
}

