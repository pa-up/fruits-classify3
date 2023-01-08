from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('classify_app.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Htmlレスポンスをmediaに格納

# 管理者が画像を表示
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
