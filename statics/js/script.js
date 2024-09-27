window.addEventListener("load", () => {
    const texts = document.querySelectorAll('input[type="text"]');
    const textareas = document.querySelectorAll('textarea');
    const numbers = document.querySelectorAll('input[type="number"]');
    const urls = document.querySelectorAll('input[type="url"]');
    console.log("Nombre d'inputs de type texte sélectionnés :", texts.length);
    console.log("Nombre de textarea sélectionnés :", textareas.length);
    for (let input of texts) {
        input.classList.add("block", "w-full", "rounded-md", "border", "py-1.5", "text-gray-900", "shadow-sm", "ring-1", "ring-inset", "ring-gray-300", "placeholder:text-gray-400", "focus:ring-2", "focus:ring-inset", "focus:ring-indigo-600", "sm:text-sm", "sm:leading-6");
    }

    for (let number of numbers) {
        number.classList.add("block", "w-full", "rounded-md", "border", "py-1.5", "text-gray-900", "shadow-sm", "ring-1", "ring-inset", "ring-gray-300", "placeholder:text-gray-400", "focus:ring-2", "focus:ring-inset", "focus:ring-indigo-600", "sm:text-sm", "sm:leading-6");
    }

    for (let url of urls) {
        url.classList.add("block", "w-full", "rounded-md", "border", "py-1.5", "text-gray-900", "shadow-sm", "ring-1", "ring-inset", "ring-gray-300", "placeholder:text-gray-400", "focus:ring-2", "focus:ring-inset", "focus:ring-indigo-600", "sm:text-sm", "sm:leading-6");
    }

    for (let textarea of textareas) {
        textarea.classList.add("block", "w-full", "rounded-md", "border", "py-1.5", "text-gray-900", "shadow-sm", "ring-1", "ring-inset", "ring-gray-300", "placeholder:text-gray-400", "focus:ring-2", "focus:ring-inset", "focus:ring-indigo-600", "sm:text-sm", "sm:leading-6");
    }

    new TomSelect("select", {
        persist: false,
        createOnBlur: true,
        // create: true
    });

    const relatedWidgetWrapper = document.querySelector(".related-widget-wrapper");
    if (relatedWidgetWrapper) {
        relatedWidgetWrapper.classList.add("flex", "flex-col", "gap-2", "flex-shrink-0");
    }
})
