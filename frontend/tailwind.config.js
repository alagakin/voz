export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [
      function ({ addBase, addUtilities }) {
      addBase({
        'body': { // Apply the styles to the body element
          '::-webkit-scrollbar': {
            width: '6px', // Width of the scrollbar
          },
          '::-webkit-scrollbar-thumb': {
            backgroundColor: 'transparent', // Color of the thumb (scrollbar handle)
            borderRadius: '3px', // Rounded corners for the thumb
          },
          '::-webkit-scrollbar-track': {
            backgroundColor: 'transparent', // Color of the track (the area behind the thumb)
            borderRadius: '3px', // Rounded corners for the track
          },
        },
      });
    },
  ],
}