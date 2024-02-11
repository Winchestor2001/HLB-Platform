/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            keyframes: {
                "right": {
                    "0%": { transform: "translateX(15%)" },
                    "50%": { transform: "translateX(0%)" },
                    "100%": { transform: "translateX(15%)" }
                }
            },
            animation: {
                "right": "right 2s ease-in-out infinite"
            }
        },
    },
    plugins: [],
}