console.log('Update that Cart')

var updateBtn = document.getElementsByClassName('update-cart')

for(i = 0; i < updateBtn.length; i++){
    updateBtn[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, 'action:', action)
        console.log('USER:', user)

        if(user == 'AnonymousUser'){
            addCookieItem(productId, action)
        }else{
            updateItem(productId, action)
        }
    })
}

function updateItem(productId, action){
    console.log('User is authenticated, sending data...')

    var url = '/update-item/'
    fetch(url, {method:'POST', headers:{'Content-Type':'application/json', 'X-CSRFToken':csrftoken,}, body:JSON.stringify({'productId':productId, 'action':action})})
    .then((response) => {return response.json()})
    .then((data) => {
        console.log('Data:', data)
        location.reload()
    })
}

function addCookieItem(productId, action){
    console.log('User is not authenticated, sending data....')
    
    if(action == 'add'){
        if(cart[productId] == undefined){
            cart[productId] = {'quantity': 1}
        }else{
            cart[productId]['quantity'] += 1
        }
    }
    if(action == 'remove'){
        cart[productId]['quantity'] -= 1

        if(cart[productId]['quantity'] <= 0){
            console.log('Item should be deleted')
            delete cart[productId];
        }
    }
    console.log('Cart:', cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
}