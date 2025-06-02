def get_response(category: str) -> str:
    responses = {
        "dasturlash": "Siz dasturlash bo‘yicha savol berdingiz. Javob: bu mavzu bo‘yicha ko‘proq ma’lumot olish uchun Python.org saytiga qarang.",
        "matematika": "Bu matematika mavzusiga oid savol. Javob: integrallar aniq va noaniq bo‘lishi mumkin.",
        "tarix": "Savolingiz tarix bilan bog‘liq. Javob: Temuriylar davri o‘rta asrlarda Markaziy Osiyoda bo‘lgan."
    }
    return responses.get(category, "Bu bo‘yicha hali ma’lumotlar bazasida javob yo‘q.")
