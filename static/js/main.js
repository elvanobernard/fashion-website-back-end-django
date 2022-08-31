function getCookie(name){
    if(document.cookie && document.cookie != ''){
        const cookies = document.cookie.split(';');
        for(let i = 0; i < cookies.length; i++){
            const cookie = cookies[i].trim();
            if(cookie.substring(0, name.length+1) === (name + '=')){
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break
            }
        }
    }
    
    return cookieValue
}

const csrftoken = getCookie('csrftoken');


(function ($) {
    "use strict";
    
    // Dropdown on mouse hover
    $(document).ready(function () {
        function toggleNavbarMethod() {
            if ($(window).width() > 992) {
                $('.navbar .dropdown').on('mouseover', function () {
                    $('.dropdown-toggle', this).trigger('click');
                }).on('mouseout', function () {
                    $('.dropdown-toggle', this).trigger('click').blur();
                });
            } else {
                $('.navbar .dropdown').off('mouseover').off('mouseout');
            }
        }
        toggleNavbarMethod();
        $(window).resize(toggleNavbarMethod);
    });
    
    
    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 100) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
        return false;
    });


    // Vendor carousel
    $('.vendor-carousel').owlCarousel({
        loop: true,
        margin: 29,
        nav: false,
        autoplay: true,
        smartSpeed: 1000,
        responsive: {
            0:{
                items:2
            },
            576:{
                items:3
            },
            768:{
                items:4
            },
            992:{
                items:5
            },
            1200:{
                items:6
            }
        }
    });


    // Related carousel
    $('.related-carousel').owlCarousel({
        loop: true,
        margin: 29,
        nav: false,
        autoplay: true,
        smartSpeed: 1000,
        responsive: {
            0:{
                items:1
            },
            576:{
                items:2
            },
            768:{
                items:3
            },
            992:{
                items:4
            }
        }
    });


    // Product Quantity
    $('.quantity button').on('click', function () {
        var button = $(this);
        var oldValue = button.parent().parent().find('input').val();
        if (button.hasClass('btn-plus')) {
            var newVal = parseFloat(oldValue) + 1;
        } else {
            if (oldValue > 0) {
                var newVal = parseFloat(oldValue) - 1;
            } else {
                newVal = 0;
            }
        }
        button.parent().parent().find('input').val(newVal);
    });
    
    $('#add-to-cart').on('click', function(){
        const target_id = this.dataset.id;
        const price = this.dataset.price;
        const quantity = parseInt($('#order-quantity').val());
        $.post("/cart", {
            'csrfmiddlewaretoken': csrftoken,
            'product-id': target_id,
            'quantity': quantity,
            'price': price,
            'action': 'add'
        }).done(function(data){
            console.log(data);
            if(parseInt(data) === 200){
                alert('Item added to cart');
            }
        });
    })

    const delete_from_cart = function(element, target_id, quantity, price){
        $.post("/cart", {
            'csrfmiddlewaretoken': csrftoken,
            'product-id': target_id,
            'quantity': quantity,
            'price': price,
            'action': 'del'
        }).done(function(data){
            data = JSON.parse(data)
            $('#cart-sub-total').text(data.subtotal)
            $('#cart-total').text(data.subtotal)
            $(element).remove()
        })
    };

    $('.product-quantity').change(function(){
        const parents = $(this).parents('.cart-row')[0];
        const quantity = parseInt($(this).val());
        const target_id =  parents.dataset.id;
        const price = parseInt(this.dataset.price);
        const current_el = this;
        if(quantity === 0){
            delete_from_cart(parents, target_id, quantity, price)
        } else {
            $.post("/cart", {
                'csrfmiddlewaretoken': csrftoken,
                'product-id': target_id,
                'quantity': quantity,
                'price': price,
                'action': 'mod'
            }).done(function(data){
                data = JSON.parse(data)
                $(current_el).parents('td').siblings('#total-price').text('$' +(quantity * price));
                $('#cart-sub-total').text(data.subtotal)
                $('#cart-total').text(data.subtotal)
            });
        }

    })

    $('.cart-plus-btn, .cart-minus-btn').click(function(){
        const parents = $(this).parents('.cart-row')[0];
        const input = $(this).parents('div').siblings('input')[0];
        const quantity = parseInt($(input).val());
        const target_id =  parents.dataset.id;
        const current_el = this;
        const price = parseInt(parents.dataset.price);
        if(quantity === 0){
            delete_from_cart(parents, target_id, quantity, price)
        } else {
            $.post("/cart", {
                'csrfmiddlewaretoken': csrftoken,
                'product-id': target_id,
                'quantity': quantity,
                'price': price,
                'action': 'mod'
            }).done(function(data){
                data = JSON.parse(data)
                $(current_el).parents('td').siblings('#total-price').text('$' +(quantity * price));
                $('#cart-sub-total').text(data.subtotal)
                $('#cart-total').text(data.subtotal)
            });
        }

    })

    $('.del-cart-btn').click(function(){
        const parents = $(this).parents('.cart-row')[0];
        const target_id =  parents.dataset.id;
        const price = parseInt(parents.dataset.price);
        const quantity = $(this).parents('td').siblings('#input-column').find('input').val();
        delete_from_cart(parents, target_id, quantity, price)

    });

    $('.place-order-btn').click(function(){
        console.log('Button clicked');
        console.log($('#buyer-data-form'));
        $('#buyer-data-form')[0].submit();
    });

    

    const submit_filter = function(){
        const url = new URL($(location).attr('href'));
        const context = {
            'csrfmiddlewaretoken': csrftoken,
            'filter': ""
        }

        const filter = []
        // If all price filter not checked, obtain all price range that want to be filtered
        if(!$('#price-all')[0].checked){
            for(let i = 1; i <= $('.price-filter-id').length; i++){
                if($(`#price-${i}`)[0].checked){
                    filter.push($(`#price-${i}`)[0].value);
                }
            }

        }

        context['filter'] = filter.toString();

        // $.post(url.pathname, context)
        $("#products-container").html('').load(url.pathname, context);
    }

    // Check/Uncheck Price Filter
    // Unchecking all other price filter if "all price" filter is checked
    $('#price-all').change(function(){
        console.log('price-all changed');
        if(this.checked){
            for(let i = 1; i <= $('.price-filter-id').length; i++){
                $(`#price-${i}`)[0].checked = false;
            }
        }
        
        submit_filter();
    })

    $('.price-filter-id').change(function(){
        if(this.checked){
            // Unchecking 'all price' filter if any other price filter is checked
            $(`#price-all`)[0].checked = false;
        } else {
            // Checking if there are any checked filter. If none, check 'all price'
            let filter_checked = false;
            for(let i = 1; i <= $('.price-filter-id').length; i++){
                if($(`#price-${i}`)[0].checked){
                    filter_checked = true;
                    break;
                }
            }

            if(!filter_checked) $(`#price-all`)[0].checked = true;
        }
        
        submit_filter();
    })

})(jQuery);

