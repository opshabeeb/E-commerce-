from . models import *
from cart.cart import Cart
# def add_variable_to_context(request):
#     return{
#         'wish_count':Wishlist.objects.filter(user=request.user)
#     }
def wishlist_item_count(request):
    wishlist_count = 0
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.filter(user=request.user).first()
        if wishlist:
            wishlist_count = wishlist.products.count()  # Assuming 'products' is the related name for the items in the wishlist
    return {'wishlist_item_count': wishlist_count}


