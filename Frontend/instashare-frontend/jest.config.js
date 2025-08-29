/** @type {import('jest').Config} **/
module.exports = {
  preset: 'ts-jest',
  testEnvironment: "jest-environment-jsdom",
  globals: {
    "import": {
      "meta": {
        env: {
          VITE_SUPABASE_URL: "http://localhost:54321",
          VITE_SUPABASE_ANON_KEY: "test-key",
          VITE_API_URL: "http://localhost:8000",
        },
      },
   }
  },
  transform: {
    '^.+\\.(ts|tsx)$': [
      'ts-jest',
      {
        tsconfig: {
          module: "ESNext",
          target: "ESNext",
        },
        diagnostics: {
          ignoreCodes: [1343]
        },
        astTransformers: {
          before: [
            {
              path: 'node_modules/ts-jest-mock-import-meta',  // or, alternatively, 'ts-jest-mock-import-meta' directly, without node_modules.
              options: { metaObjectReplacement: { 
                url: 'https://www.url.com',
                env: {
                VITE_API_URL: 'https://www.url.com',
               } 
              }
             }
            }
          ]
        }
      },
    ],
    
    //"^.+\\.[t|j]sx?$": "babel-jest"
  },
  transformIgnorePatterns: [
    "/node_modules/(?!(@supabase/supabase-js|@supabase/auth-ui-react|@supabase/auth-ui-shared|react-router-dom|react-router|react-icons|@react-hook)/)",
  ],
  moduleNameMapper: {
    "\\.css$": "identity-obj-proxy",
    "^@/(.*)$": "<rootDir>/src/$1",
    "^@/services/api$": "<rootDir>/src/mocks/api.ts",
    "^@/contexts/AuthContext$": "<rootDir>/src/mocks/AuthContext.tsx",
  },
  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json', 'node'],
  extensionsToTreatAsEsm: ['.ts', '.tsx'],
  setupFilesAfterEnv: ["<rootDir>/src/setupTests.ts"],
};