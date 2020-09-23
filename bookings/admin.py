from django.contrib import admin
from bookings.models import Lesson, Voucher, VoucherUser, UserLesson


class VoucherUserAdmin(admin.ModelAdmin):
    readonly_fields = ('used',)


admin.site.register(Lesson)
admin.site.register(Voucher)
admin.site.register(VoucherUser, VoucherUserAdmin)
admin.site.register(UserLesson)
