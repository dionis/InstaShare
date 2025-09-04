import '@testing-library/jest-dom';
import { TextEncoder, TextDecoder } from 'text-encoding';

Object.defineProperty(global, 'TextEncoder', {
  writable: true,
  value: TextEncoder,
});

Object.defineProperty(global, 'TextDecoder', {
  writable: true,
  value: TextDecoder,
});






