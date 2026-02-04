from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.shop.models import Product
from .models import Review, ReviewVote


@login_required(login_url='login')
def add_review(request, product_id):
    """Add or update a review"""
    product = get_object_or_404(Product, id=product_id)
    review = Review.objects.filter(product=product, user=request.user).first()

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        rating = int(request.POST.get('rating'))

        if review:
            review.title = title
            review.content = content
            review.rating = rating
            review.save()
            messages.success(request, 'Review updated successfully!')
        else:
            review = Review.objects.create(
                product=product,
                user=request.user,
                title=title,
                content=content,
                rating=rating
            )
            messages.success(request, 'Review added successfully!')

        return redirect('product_detail', slug=product.slug)

    context = {'product': product, 'review': review}
    return render(request, 'reviews/add_review.html', context)


@login_required(login_url='login')
def delete_review(request, review_id):
    """Delete a review"""
    review = get_object_or_404(Review, id=review_id, user=request.user)
    product_slug = review.product.slug
    review.delete()
    messages.success(request, 'Review deleted successfully!')
    return redirect('product_detail', slug=product_slug)


@login_required(login_url='login')
def vote_helpful(request, review_id):
    """Mark review as helpful"""
    review = get_object_or_404(Review, id=review_id)

    vote, created = ReviewVote.objects.get_or_create(
        review=review,
        user=request.user,
        defaults={'vote_type': 'helpful'}
    )

    if not created:
        if vote.vote_type == 'helpful':
            vote.delete()
        else:
            vote.vote_type = 'helpful'
            vote.save()

    return redirect('product_detail', slug=review.product.slug)


@login_required(login_url='login')
def vote_unhelpful(request, review_id):
    """Mark review as unhelpful"""
    review = get_object_or_404(Review, id=review_id)

    vote, created = ReviewVote.objects.get_or_create(
        review=review,
        user=request.user,
        defaults={'vote_type': 'unhelpful'}
    )

    if not created:
        if vote.vote_type == 'unhelpful':
            vote.delete()
        else:
            vote.vote_type = 'unhelpful'
            vote.save()

    return redirect('product_detail', slug=review.product.slug)
