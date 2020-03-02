$(function() {
    // $('.nav a').on('click',function(){
    //             $(this).tab('show');
    //         })

    // 修改页面页面赋值函数
    function setValue( table,pk,label,attribute,chang_class) {
        let id = '#'+table+'_'+label+'_'+pk;
        let value = $(id).text();
        $(chang_class).attr(attribute,value);
    }

    //设置select选中状态
    function setSelect( table,pk,label,chang_class) {
        let id = '.'+table+'_'+label+'_'+pk;
     $(id).each(function(){
      let tpk= $(this).attr('name');
            let chang_class_new = chang_class+tpk;
            $(chang_class_new).attr("selected", true);
    })
    }

    // 判断是不是在数组中
    function isInArray(arr,value){
        for(var i = 0; i < arr.length; i++){
            if(value === arr[i]){
                return true;
            }
        }
        return false;
    }

    // 删除函数
    function deleteData(a,b) {
        $(a).click(function() {
            let pk = $(this).attr('name');
            let url = '/book/' + pk + b;
            $.ajax({
                url: url,
                type: "get",
                data: {},
                success: function (data) {
                    console.log(data);
                    location.reload();
                }
            })
        })
    }

    //编辑书籍模态框获取数据
    $(".change_book").click(function(){
        let pk = $(this).attr('name');
        let url = '/book/'+ pk + '/change_book/';
        setValue('book',pk,'title','value',".changeBookTitle");
        setValue('book',pk,'price','value',".changeBookPrice");
        setValue('book',pk,'publishDate','value',".changeBookPublishDate");
        setSelect('book',pk,'publish',".changeBookPublish_");
        setSelect('book',pk,'author',".changeBookAuthor_");
        $(".change_book_save").attr('href',url);
        $(".change_book_save").attr('name',pk);
    })

    // 编辑书籍模态框隐藏时
    $("#change_book").on('hidden.bs.modal', function () {
        window.location.reload();
    })

    //编辑书籍设置数据
    $(".change_book_save").click(function () {
        let cb_url = $(this).attr('href');
        let data = new FormData($("#changeBookAjax")[0]);
        $.ajax({
            dataType: "json",
            url:cb_url,
            type:"post",
            contentType:false,
            processData:false,
            data: data,
            success:function(data){
                // console.log(data)
                if (data['res'] === 0) {
                    $('#change_book').modal("hide");
                    location.reload();
                } else {
                    $('.changeBookPrice').val(data['error']).css({"color":"red"});

                }

            }
        })
    })

    //新增书籍
    $(".add_book_save").click(function () {
        let data = new FormData($("#addBookAjax")[0]);
        $.ajax({
            dataType: "json",
            url:'/book/add_book/',
            type:"post",
            contentType:false,
            processData:false,
            data: data,
            success:function(data){
                // console.log(data)
                if (data['res'] === 0) {
                    $('#add_book').modal("hide");
                    location.reload();
                } else if (isInArray([10,11],data['res'])) {
                    $('.addBookTitle').val(data['error']).css({"color":"red"});
                } else if (isInArray([20,21],data['res'])) {
                    $('.addBookPrice').val(data['error']).css({"color":"red"});
                } else if (data['res'] === 30) {
                    $('.addBookPublishDate').css({"color":"red"});
                } else if (data['res'] === 40) {
                    $('.add_book_author').css({"color":"red"});
                    console.log(data['error']);
                } else if (data['res'] === 50) {
                    $('.add_book_publish').css({"color":"red"});
                    console.log(data['error']);
                }

            }
        })
    })

    //取消新增书籍模态框获取数据
    $("#add_book").on('hidden.bs.modal', function () {
        window.location.reload();
    })


    // 删除书籍
    deleteData('.delete_book','/delete_book/');


    // 编辑作者获取数据
    $(".change_author").click(function(){
        let pk = $(this).attr('name');
        let url = '/book/'+ pk + '/change_author/';
        setValue('author',pk,'name','value',".changeAuthorName");
        setValue('author',pk,'age','value',".changeAuthorAge");
        $(".change_author_save").attr('href',url);
        $(".change_author_save").attr('name',pk);
    })

    // 取消编辑作者
    $("#changeAuthor").on('hidden.bs.modal', function () {
        window.location.reload();
    })

    //编辑作者
    $(".change_author_save").click(function () {
        let cb_url = $(this).attr('href');
        let data = new FormData($("#changeAuthorAjax")[0]);
        $.ajax({
            dataType: "json",
            url:cb_url,
            type:"post",
            contentType:false,
            processData:false,
            data: data,
            success:function(data){
                console.log(data)
                if (data['res'] === 0) {
                    $('#changeAuthor').modal("hide");
                    location.reload();
                } else if (isInArray([10,11],data['res'] )) {
                    $('.changeAuthorName').val(data['error']).css({"color":"red"});

                } else if (data['res'] === 20) {
                    $('.changeAuthorAge').val(data['error']).css({"color":"red"});

                } else  {
                    console.log(data['error'])
                }

            }
        })
    })

    //增加作者
    $(".add_author_save").click(function () {
        let data = new FormData($("#addAuthorAjax")[0]);
        $.ajax({
            dataType: "json",
            url:'/book/add_author/',
            type:"post",
            contentType:false,
            processData:false,
            data: data,
            success:function(data){
                console.log(data)
                if (data['res'] === 0) {
                    $('#add_author').modal("hide");
                    location.reload();
                } else if (isInArray([10,11],data['res'] )) {
                    $('.addAuthorName').val(data['error']).css({"color":"red"});

                } else if (data['res'] === 20) {
                    $('.addAuthorAge').val(data['error']).css({"color":"red"});

                } else  {
                    console.log(data['error'])
                }

            }
        })
    })

    // 取消新建作者获取数据
    // 编辑书籍模态框隐藏时
    $("#add_author").on('hidden.bs.modal', function () {
        window.location.reload();
    })

    // 删除作者
    deleteData('.delete_author','/delete_author/');



    // 编辑出版社获取数据
    $(".change_publish").click(function(){
        let pk = $(this).attr('name');
        let url = '/book/'+ pk + '/change_publish/';
        setValue('publish',pk,'name','value',".changePublishName");
        setValue('publish',pk,'city','value',".changePublishCity");
        setValue('publish',pk,'email','value',".changePublishEmail");
        $(".change_publish_save").attr('href',url);
        $(".change_publish_save").attr('name',pk);
    })

    // 取消编辑出版社获
    $("#change_publish").on('hidden.bs.modal', function () {
        window.location.reload();
    })

    //编辑出版社
    $(".change_publish_save").click(function () {
        let cb_url = $(this).attr('href');
        let data = new FormData($("#changePublishAjax")[0]);
        $.ajax({
            dataType: "json",
            url:cb_url,
            type:"post",
            contentType:false,
            processData:false,
            data: data,
            success:function(data){
                console.log(data)
                if (data['res'] === 0) {
                    $('#change_publish').modal("hide");
                    location.reload();
                    $('#publish_tab').tab('show');
                } else if (isInArray([10,11],data['res'])) {
                    $('.changePublishName').val(data['error']).css({"color":"red"});

                } else if (data['res'] === 20) {
                    $('.changePublishCity').val(data['error']).css({"color":"red"});

                } else if (isInArray([30,31],data['res'])) {
                    $('.changePublishEmail').val(data['error']).css({"color":"red"});

                } else  {
                    console.log(data['error'])
                }

            }
        })
    })


    //增加出版社
    $(".add_publish_save").click(function () {
        let data = new FormData($("#addPublishAjax")[0]);
        $.ajax({
            dataType: "json",
            url:'/book/add_publish/',
            type:"post",
            contentType:false,
            processData:false,
            data: data,
            success:function(data){
                console.log(data)
                if (data['res'] === 0) {
                    $('#add_publish').modal("hide");
                    location.reload();
                    $('#publish_tab').tab('show');
                } else if (isInArray([10,11],data['res'])) {
                    $('.addPublishName').val(data['error']).css({"color":"red"});

                } else if (data['res'] === 20) {
                    $('.addPublishCity').val(data['error']).css({"color":"red"});

                } else if (isInArray([30,31],data['res'])) {
                    $('.addPublishEmail').val(data['error']).css({"color":"red"});

                } else  {
                    console.log(data['error'])
                }

            }
        })
    })

    // 取消时出版社获取数据
    $("#add_publish").on('hidden.bs.modal', function () {
        window.location.reload();
    })

    // 删除出版社
    deleteData('.delete_publish','/delete_publish/');


})
