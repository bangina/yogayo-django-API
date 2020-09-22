from django.contrib import admin
from bookings.models import Lesson, Voucher, VoucherUser, UserLesson


admin.site.register(Lesson)
admin.site.register(Voucher)
admin.site.register(VoucherUser)
admin.site.register(UserLesson)
