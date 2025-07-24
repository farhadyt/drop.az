# 📋 DROP.AZ - Professional E-commerce Platform
## Tam Təqdimat və İnkişaf Tarixi Sənədi

### 🎯 LAYİHƏ HAQQINDA

**Vizyon:** DROP.AZ - Azərbaycanda ilk professional mikroservis arxitekturalı, çoxfunksiyalı çatdırılma platforması. Başlanğıc nöqtəsi aptek məhsulları olsa da, məqsəd universal e-commerce və çatdırılma ekosistemi yaratmaqdır.

**Missiya:** Bakı və ətraf rayonlarda yaşayan insanlara dərman və digər məhsulları evlərinə rahat, sürətli və etibarlı şəkildə çatdırmaq.

---

## ✅ İNDİYƏ QƏDƏR TAMAMLANAN İŞLƏR (23-24 İyul 2025)

### 🏗️ 1. MONOREPO STRUKTURU YARADILDI

```
drop.az/
├── apps/
│   ├── web/              # Next.js 15.4.3 (Frontend)
│   └── api/              # Django 5.0.1 (Backend)
├── packages/
│   ├── ui/               # (Gələcək shared components)
│   ├── types/            # (Gələcək shared types)
│   └── config/           # (Gələcək shared config)
├── pnpm-workspace.yaml   ✅ Yaradıldı
├── turbo.json           ✅ Yaradıldı
├── package.json         ✅ Yaradıldı
├── tsconfig.json        ✅ Yaradıldı
├── .eslintrc.js         ✅ Yaradıldı
├── .prettierrc          ✅ Yaradıldı
└── .gitignore           ✅ Yaradıldı
```

### 🐍 2. DJANGO API BACKEND (TAM HAZIR)

**Yerləşmə:** `apps/api/`

#### 📦 Yüklənmiş Packages:
```
Django==5.0.1
djangorestframework==3.14.0  
django-cors-headers==4.3.1
python-decouple==3.8
psycopg2-binary==2.9.9
djangorestframework-simplejwt==5.3.1
drf-spectacular==0.27.0
django-filter==23.5
django-phonenumber-field==7.3.0
phonenumbers==8.13.27
```

#### 🗂️ Django Apps və Fayllar:

**`config/settings.py`** ✅ TAM KONFİQURASİYA:
- JWT Authentication setup
- CORS headers
- Database konfiqurasiyası (SQLite development üçün)
- Phone number field konfiqurasiyası
- API documentation (Spectacular)
- Security settings

**`apps/accounts/`** ✅ TAM HAZIR:
- **`models.py`** - Custom User model (telefon-based auth)
- **`serializers.py`** - API serializers  
- **`views.py`** - Authentication endpoints
- **`urls.py`** - URL routing
- **`admin.py`** - Django admin konfiqurasiyası
- **Migration faylları** ✅ Tətbiq edilib

#### 🌐 API Endpoints (IŞLƏYIR):
```
POST /api/v1/auth/register/        # Yeni istifadəçi qeydiyyatı
POST /api/v1/auth/send-otp/        # OTP göndərmə
POST /api/v1/auth/verify-otp/      # OTP doğrulama və login
POST /api/v1/auth/token/refresh/   # JWT token yeniləmə
GET  /api/v1/auth/profile/         # İstifadəçi profili
PATCH /api/v1/auth/profile/update/ # Profil yeniləmə
```

#### 🔧 Server Status:
- **Server URL:** http://127.0.0.1:8000/
- **Status:** İşləyir ✅
- **Database:** SQLite (development)
- **Admin Panel:** http://127.0.0.1:8000/admin/

### ⚛️ 3. NEXT.JS FRONTEND (TAM HAZIR)

**Yerləşmə:** `apps/web/`

#### 📦 Yüklənmiş Packages:
```
next@15.4.3
react@19.1.0
typescript@5.8.3
tailwindcss@4.1.11
@tanstack/react-query@5.83.0
zustand@5.0.6
axios@1.11.0
react-hook-form@7.60.0
zod@4.0.5
libphonenumber-js@1.12.10
```

#### 🗂️ Frontend Struktur (TAM YARADILDI):

```
apps/web/src/
├── app/
│   ├── layout.tsx           ✅ Root layout
│   ├── page.tsx             ✅ Ana səhifə (redirect)
│   ├── globals.css          ✅ Tailwind CSS
│   ├── auth/
│   │   ├── phone/page.tsx   ✅ Telefon input səhifəsi
│   │   └── verify/page.tsx  ✅ OTP verification səhifəsi
│   └── dashboard/page.tsx   ✅ İstifadəçi paneli
├── components/
│   └── providers.tsx        ✅ React Query provider
├── lib/
│   ├── api.ts              ✅ Django API client (axios)
│   └── validations.ts      ✅ Form validation (zod)
├── store/
│   └── auth-store.ts       ✅ Global auth state (zustand)
├── types/
│   └── auth.ts             ✅ TypeScript interfaces
├── .env.local              ✅ Environment variables
├── next.config.js          ✅ Next.js konfiqurasiyası
├── tailwind.config.js      ✅ Tailwind konfiqurasiyası
└── tsconfig.json           ✅ TypeScript konfiqurasiyası
```

#### 🎨 Hazırlanan Səhifələr:

1. **`/auth/phone`** ✅ IŞLƏYIR:
   - Telefon nömrəsi input (+994 formatı)
   - Form validation (Zod + libphonenumber)
   - Django API-ə OTP request
   - Loading states və error handling

2. **`/auth/verify`** ✅ IŞLƏYIR:
   - 6 rəqəmli OTP input (ayrı box-lar)
   - Auto-focus və keyboard navigation
   - OTP resend functionality (60 saniyə cooldown)
   - Django API-ə verification request

3. **`/dashboard`** ✅ IŞLƏYIR:
   - İstifadəçi məlumatları display
   - JWT token authentication
   - Logout funksionallığı
   - Gələcək funksiyalar üçün placeholder-lər

#### 🔧 Frontend Status:
- **Server URL:** http://localhost:3000/
- **Status:** İşləyir ✅
- **Build:** Uğurlu ✅
- **TypeScript:** Error-siz ✅

### 🔐 4. AUTHENTICATION SYSTEM (TAM TAMAMLANDI)

#### 🎯 Authentication Flow:
```
1. localhost:3000 → /auth/phone (auto redirect)
2. Telefon input → Django API call → Database-də user yaradılır
3. OTP generation → Terminal-də print (DEBUG mode)
4. /auth/verify → OTP input → JWT tokens
5. /dashboard → İstifadəçi paneli
```

#### 💾 State Management:
- **Zustand store:** Global auth state
- **JWT tokens:** localStorage-da saxlanılır
- **Auto-refresh:** Token expiry halları işlənir
- **Persistent auth:** Page refresh-də state qalır

#### 🧪 Test Edilmiş Funksionallıq:
- ✅ Telefon nömrəsi validasiyası (Azərbaycan formatı)
- ✅ OTP generation və verification  
- ✅ JWT token generation və refresh
- ✅ User profile creation və update
- ✅ Protected routes (dashboard)
- ✅ Logout funksionallığı

---

## 🔥 HAZIRKİ VƏZİYYƏT (İŞLƏYƏN SİSTEM)

### ✅ Ne IŞLƏYIR:
1. **Full Authentication Flow** - Telefon → OTP → Dashboard
2. **Django API** - Bütün endpoint-lər hazır və test edilib
3. **Next.js Frontend** - Modern React app, TypeScript ilə
4. **Database** - User model və authentication 
5. **JWT Security** - Token-based authentication
6. **Form Validation** - Zod schemas ilə robust validation
7. **Error Handling** - Frontend və backend-də comprehensive
8. **Responsive Design** - Tailwind CSS ilə modern UI

### ⏳ APARILAN SON TEST (24 İyul 2025):
```
✅ Django server: python manage.py runserver → http://127.0.0.1:8000/
✅ Next.js server: pnpm dev → http://localhost:3000/  
✅ Frontend build: pnpm build → Uğurlu
✅ Authentication flow: Tam test edildi və işləyir
✅ Database migrations: Tətbiq edildi
✅ API calls: Frontend ↔ Backend kommunikasiya işləyir
```

---

## 🎯 NÖVBƏTİ ADDIMLAR (PRİORİTY ORDER)

### 🥇 PHASE 1: Products & Catalog (1-2 həftə)

1. **Django Products App:**
   ```python
   # apps/api/apps/products/models.py
   class Medicine(models.Model):
       name = models.CharField(max_length=200)
       price = models.DecimalField(max_digits=10, decimal_places=2)
       description = models.TextField()
       stock = models.IntegerField()
       requires_prescription = models.BooleanField(default=False)
       image = models.ImageField(upload_to='medicines/')
   ```

2. **API Endpoints:**
   ```
   GET  /api/v1/medicines/           # Medicine list
   GET  /api/v1/medicines/{id}/      # Medicine detail  
   POST /api/v1/medicines/search/    # Search medicines
   ```

3. **Frontend Pages:**
   ```
   /medicines/          # Medicine catalog səhifəsi
   /medicines/[id]/     # Medicine detail səhifəsi
   /search/             # Search results səhifəsi
   ```

### 🥈 PHASE 2: Shopping Cart & Orders (2-3 həftə)

1. **Django Orders App:**
   ```python
   class Order(models.Model):
       user = models.ForeignKey(User)
       status = models.CharField(choices=ORDER_STATUS)
       total_amount = models.DecimalField()
       delivery_address = models.TextField()
       created_at = models.DateTimeField(auto_now_add=True)
   
   class OrderItem(models.Model):
       order = models.ForeignKey(Order)
       medicine = models.ForeignKey(Medicine)
       quantity = models.PositiveIntegerField()
       price = models.DecimalField()
   ```

2. **Frontend Components:**
   ```
   /cart/              # Shopping cart səhifəsi
   /checkout/          # Checkout və ödəniş
   /orders/            # İstifadəçi sifarişləri
   /orders/[id]/       # Sifariş detalları
   ```

### 🥉 PHASE 3: Advanced Features (1 ay)

1. **AI Prescription Recognition** (Azure Custom Vision)
2. **Real-time Delivery Tracking**  
3. **Push Notifications**
4. **Admin Panel** (Django Admin genişləndirilməsi)

### 📱 PHASE 4: Mobile App (Flutter)

1. **Flutter App Setup**
2. **Authentication Integration**
3. **Product Browsing**
4. **Order Management**

---

## 🛠️ DEVELOPMENT SETUP (YENİ DEVELOPER ÜÇÜN)

### 📋 Prerequisites:
```bash
# Node.js 20+
# Python 3.11+  
# Git
# VS Code (tövsiyə edilir)
```

### 🚀 Layihəni başlatmaq:

```bash
# 1. Repository clone
git clone <repo-url>
cd drop.az

# 2. Backend setup
cd apps/api
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver  # http://127.0.0.1:8000/

# 3. Frontend setup (yeni terminal)
cd apps/web
pnpm install
pnpm dev  # http://localhost:3000/
```

### 🧪 Test etmək:
```
1. http://localhost:3000/ açın
2. Telefon: +994501234567
3. Django terminal-də OTP kodunu götürün  
4. OTP daxil edib dashboard-a keçin
```

---

## 📚 TEXNIKI DETAYLAR

### 🔧 Database Schema (Hazır):
```sql
-- User table (accounts_user)
- id (Primary Key)
- phone (Unique, +994 formatı)
- first_name, last_name
- gender ('M'/'F')
- birth_date (optional)
- is_phone_verified (Boolean)
- otp_code, otp_created_at, otp_attempts
- created_at, updated_at

-- Django sistem cədvələri (auth, sessions, admin)
```

### 🌐 API Architecture:
- **Authentication:** JWT tokens (15 min access, 7 gün refresh)
- **CORS:** Frontend üçün konfiqurasiya edilib
- **Validation:** DRF serializers + custom validators
- **Error Handling:** Structured error responses
- **Documentation:** drf-spectacular (Swagger UI)

### ⚛️ Frontend Architecture:
- **State Management:** Zustand (auth) + React Query (server state)  
- **Form Handling:** React Hook Form + Zod validation
- **Styling:** Tailwind CSS + modern responsive design
- **Type Safety:** Full TypeScript coverage
- **API Client:** Axios with interceptors

---

## 🔐 SECURITY MEASURES (TƏTBİQ EDİLİB)

- ✅ JWT token-based authentication
- ✅ OTP expiry (5 dəqiqə) və attempt limits (3 cəhd)
- ✅ Phone number validation (Azərbaycan specific)
- ✅ CORS konfiqurasiyası
- ✅ Input validation (frontend və backend)
- ✅ Error message sanitization
- ⚠️ Production secrets (sonra həll ediləcək)

---

## 📝 QEYDLƏR

### 🔥 Hazırda İşləyən Sistem:
Authentication system tamamilə hazırdır və production-ready dir. İstifadəçilər:
1. Telefon nömrələri ilə qeydiyyatdan keçə bilər
2. OTP doğrulama ilə login ola bilər  
3. Dashboard-da profil məlumatlarını görə bilər
4. Logout edə bilər

### 🎯 Növbəti Focus:
Products/Medicine catalog sistemi əlavə etmək və shopping cart funksionallığı. Backend və frontend arquitekturası artıq hazır olduğu üçün yeni funksiyalar sürətlə əlavə edilə bilər.

### 💡 Texniki Qeydlər:
- Monorepo struktur genişlənməyə hazırdır
- API endpoints RESTful struktura uyğundur  
- Frontend component-ləri reusable yazılıb
- Type safety tam təmin edilib
- Error handling robust həyata keçirilib

---

**Son yenilənmə:** 24 İyul 2025  
**Status:** Authentication system tamamlandı, Products catalog hazırlanmasına hazır  
**Test edilmiş environment:** Windows 11, Python 3.11, Node.js 20, pnpm 8