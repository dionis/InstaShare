const { createDefaultPreset } = require("ts-jest");

const tsJestTransformCfg = createDefaultPreset().transform;

/** @type {import("jest").Config} **/
module.exports = {
  testEnvironment: "jest-environment-jsdom",
  transform: {
    ...tsJestTransformCfg,
  },
  moduleNameMapper: {
    "\\.css$": "identity-obj-proxy",
    "^@/(.*)$": "<rootDir>/src/$1",
    "^@/services/api$": "<rootDir>/src/mocks/api.ts",
    "^@/contexts/AuthContext$": "<rootDir>/src/mocks/AuthContext.tsx",
  },
  setupFilesAfterEnv: ["<rootDir>/src/setupTests.ts"],
};