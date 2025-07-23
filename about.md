📋 DROP.AZ - Professional E-commerce Platform
Tam Təqdimat və Texniki Sənəd

📑 MÜNDƏRİCAT

Layihə Haqqında
Biznes Modeli və Vizyon
Funksional Xüsusiyyətlər
Texniki Arxitektura
İndiyə Qədər Görülən İşlər
Növbəti Addımlar
Texnologiya Stack
Deployment və İnfrastruktur


🎯 LAYİHƏ HAQQINDA
Vizyon
DROP.AZ - Azərbaycanda ilk professional mikroservis arxitekturalı, çoxfunksiyalı çatdırılma platforması. Başlanğıc nöqtəsi aptek məhsulları olsa da, məqsəd universal e-commerce və çatdırılma ekosistemi yaratmaqdır.
Missiya
Bakı və ətraf rayonlarda yaşayan insanlara dərman və digər məhsulları evlərinə rahat, sürətli və etibarlı şəkildə çatdırmaq.
Unikal Dəyər Təklifi

🏥 Resept tanıma AI sistemi
🚴 Gündə 3 dəfə toplanmış çatdırılma
💊 Dərman xatırlatma sistemi
👨‍👩‍👧‍👦 Ailə sağlamlıq profili


💼 BİZNES MODELİ
Fazalı İnkişaf Strategiyası
Faza 1: Aptek (0-6 ay)

Lokal aptek məhsulları
Resept çatdırılması
Dərman abunəlik sistemi

Faza 2: Genişlənmə (6-12 ay)

Qida məhsulları
Gündəlik ehtiyaclar
Partner apteklər

Faza 3: Universal Platform (12+ ay)

Tikinti materialları
Elektronika
B2B xidmətlər

Gəlir Modelləri

Çatdırılma haqqı - hər sifarişdən
Abunəlik paketi - aylıq unlimited çatdırılma
Komissiya - partner satıcılardan
Premium xidmətlər - 30 dəqiqə express çatdırılma


🚀 FUNKSİONAL XÜSUSİYYƏTLƏR
🔐 İstifadəçi İdarəetmə

Telefon nömrəsi ilə qeydiyyat
SMS OTP doğrulama
Ailə profili (uşaqlar, yaşlılar üçün ayrı)
Tibbi tarixçə

🏥 Aptek Funksiyaları

AI Resept Tanıma

Kamera ilə resept skan
Azure Custom Vision inteqrasiya
Manual düzəliş imkanı


Dərman Kataloqu

Axtarış və filtr
Analoqları göstərmə
Stok statusu real-time


Dərman Xatırlatma

Push notification
WhatsApp inteqrasiya
Ailə üzvləri üçün ayrı



📦 Sifariş və Çatdırılma

Toplanmış Çatdırılma

Gündə 3 dəfə (səhər, günorta, axşam)
Rayon bazlı qruplaşdırma


Express Çatdırılma

30 dəqiqə (premium)


Order Tracking

Real-time status
Kuryer lokasiyası



💰 Ödəniş və Loyalty

Nağd ödəniş
Onlayn ödəniş (Kapital, Payriff)
Cashback sistemi (3-5%)
Referral bonusları

📱 Platform Xüsusiyyətləri

Qrup Alışı

Qonşularla birləşmə
Çatdırılma haqqı bölüşmə


Dərman Bağışlama

İstifadə olunmamış dərmanlar
Sosial məsuliyyət balları


Virtual Aptek Məsləhətçisi

24/7 AI chat
Əsas suallar üçün cavablar




🏗️ TEXNİKİ ARXİTEKTURA
Monorepo Strukturu
drop.az/
├── apps/
│   ├── web/              # Next.js 14 (müştəri interfeysi)
│   ├── admin/            # Admin panel
│   ├── api/              # Django REST API
│   └── mobile/           # Flutter mobile app
├── packages/
│   ├── ui/               # Shared React components
│   ├── types/            # TypeScript type definitions
│   └── config/           # Shared configurations
├── infrastructure/
│   ├── docker/           # Docker configurations
│   ├── k8s/              # Kubernetes manifests
│   └── terraform/        # Infrastructure as Code
└── docs/                 # Documentation
Mikroservis Arxitekturası
mermaidgraph TD
    A[API Gateway] --> B[Identity Service]
    A --> C[Catalog Service]
    A --> D[Order Service]
    A --> E[Delivery Service]
    A --> F[Notification Service]
    
    B --> G[(PostgreSQL)]
    C --> G
    C --> H[(Redis Cache)]
    D --> G
    E --> G
    F --> I[SMS Provider]
    F --> J[WhatsApp API]
Technology Stack
Frontend:

Next.js 14 (App Router, SSR)
TypeScript
Tailwind CSS
Radix UI
React Query

Backend:

Django 5.0 + Django REST Framework
PostgreSQL + Redis
Celery (background tasks)
JWT Authentication

Mobile:

Flutter 3.x
Bloc Pattern
Dio (HTTP client)

Infrastructure:

Docker + Docker Compose
GitHub Actions (CI/CD)
Vercel (Next.js hosting)
Railway/Render (Django hosting)


✅ İNDİYƏ QƏDƏR GÖRÜLƏN İŞLƏR
1. Monorepo Qurulumu ✓
bash# Yaradılan struktur
drop.az/
├── apps/web/
├── apps/api/
├── packages/ui/
├── packages/types/
├── pnpm-workspace.yaml
├── turbo.json
└── package.json
2. Development Environment ✓

pnpm package manager
Turborepo build system
TypeScript configuration
ESLint + Prettier
Git version control

3. Kod Keyfiyyət Alətləri ✓

Husky pre-commit hooks
Lint-staged
TypeScript strict mode
Path aliases configuration


📅 NÖVBƏTİ ADDIMLAR
Yaxın Müddət (1-2 həftə)

Django API Qurulumu
bashcd apps/api
python -m venv venv
pip install django djangorestframework
django-admin startproject drop_api .

Next.js Web App
bashcd apps/web
npx create-next-app@latest . --typescript --tailwind --app

Database Schema

User model (phone, OTP)
Product model
Order model
Delivery zones



Orta Müddət (1 ay)

Authentication System

SMS OTP integration
JWT tokens
Refresh token mechanism


Product Catalog

Admin panel
Search functionality
Image upload


Order Management

Cart functionality
Order placement
Status tracking



Uzun Müddət (3 ay)

AI Resept Tanıma

Azure Custom Vision setup
Training data collection
Integration with order flow


Flutter Mobile App

Authentication
Product browsing
Order placement


Delivery System

Zone management
Route optimization
Real-time tracking




🚀 DEPLOYMENT STRATEGİYASI
Development Environment
yaml# docker-compose.yml
services:
  web:
    build: ./apps/web
    ports: ["3000:3000"]
  
  api:
    build: ./apps/api
    ports: ["8000:8000"]
  
  postgres:
    image: postgres:15
  
  redis:
    image: redis:7
Production Deployment
Phase 1: MVP

Vercel (Next.js)
Railway (Django + PostgreSQL)
Upstash (Redis)

Phase 2: Scale

AWS/Azure Kubernetes
CloudFront CDN
RDS PostgreSQL


📊 PERFORMANS HƏDƏFLƏRİ

Page Load: < 2 saniyə
API Response: < 200ms
Uptime: 99.9%
Concurrent Users: 10,000+


👥 KOMANDA TƏRKİBİ (Tövsiyə)

Full-Stack Developer (1-2 nəfər)
Mobile Developer (1 nəfər)
UI/UX Designer (1 nəfər)
DevOps Engineer (part-time)


📝 QEYDLƏR
Bu sənəd canlı bir sənəddir və layihə inkişaf etdikcə yenilənəcək. Hər sprint sonunda bu sənədi update etmək tövsiyə olunur.