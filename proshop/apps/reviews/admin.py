from django.contrib import admin
from .models import Review, ReviewImage, ReviewVote


class ReviewImageInline(admin.TabularInline):
    model = ReviewImage
    extra = 1


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'product', 'user', 'rating', 'verified_purchase', 'helpful_count', 'created_at')
    list_filter = ('rating', 'verified_purchase', 'created_at')
    search_fields = ('title', 'content', 'user__username', 'product__name')
    readonly_fields = ('helpful_count', 'created_at', 'updated_at')
    inlines = [ReviewImageInline]


@admin.register(ReviewImage)
class ReviewImageAdmin(admin.ModelAdmin):
    list_display = ('review', 'created_at')
    list_filter = ('created_at',)


@admin.register(ReviewVote)
class ReviewVoteAdmin(admin.ModelAdmin):
    list_display = ('review', 'user', 'vote_type', 'created_at')
    list_filter = ('vote_type', 'created_at')
    search_fields = ('user__username', 'review__title')
