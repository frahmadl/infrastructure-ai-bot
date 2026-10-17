# 🚀 Infrastructure AI Query Bot

نظام استعلام ذكي للبنية التحتية يعتمد على **FastAPI** و **Pandas** والذكاء الاصطناعي (**OpenAI API**) لتحليل الأسئلة الطبيعية والبحث الذكي داخل بيانات السيرفرات.

---

## 🧠 فكرة المشروع

يوفر هذا المشروع واجهة برمجية (API) وواجهة تفاعلية للاستعلام عن بيانات السيرفرات المخزنة داخل ملف **Excel**، مع دعم:
* 💬 محادثة ذكاء اصطناعي مع ذاكرة (`/api/chat`)
* 🤖 استعلام ذكي يفهم الأسئلة الطبيعية (`/api/query`)
* 🔍 فلترة متقدمة حسب IP / Port / Environment / Destination
* 📊 عرض جميع السيرفرات والإحصائيات
* 📄 واجهة توثيق Swagger تفاعلية جاهزة

---

## 🛠️ المتطلبات التشغيلية

* Python 3.10+
* FastAPI
* Uvicorn
* Pandas
* OpenPyXL
* OpenAI API Key
* ملف Excel: `Training_Servers_80Rows.xlsx`

---

## 📦 تثبيت المكتبات

```bash
pip install fastapi uvicorn pandas openpyxl python-dotenv openai

## 👩‍💻 فريق المطورين (Developers)

تم تطوير هذا المشروع بواسطة فريق العمل:

* **فجر**
* **الجوهره**
* **شجون**
* **وسن**
* **ابرار**
* **يارا**
