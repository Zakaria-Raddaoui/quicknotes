import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from './App';

// Mock fetch
global.fetch = jest.fn();

beforeEach(() => {
  fetch.mockClear();
});

test('renders Quick Notes heading', () => {
  fetch.mockResolvedValueOnce({
    ok: true,
    json: async () => []
  });

  render(<App />);
  const headingElement = screen.getByText(/quick notes/i);
  expect(headingElement).toBeInTheDocument();
});

test('displays loading state initially', () => {
  fetch.mockImplementationOnce(() => new Promise(() => {}));

  render(<App />);
  expect(screen.getByText(/loading notes/i)).toBeInTheDocument();
});

test('displays empty state when no notes exist', async () => {
  fetch.mockResolvedValueOnce({
    ok: true,
    json: async () => []
  });

  render(<App />);

  await waitFor(() => {
    expect(screen.getByText(/no notes yet/i)).toBeInTheDocument();
  });
});

test('displays notes when they exist', async () => {
  const mockNotes = [
    { id: 1, title: 'Test Note', content: 'Test content', created_at: '2024-01-01T00:00:00Z' }
  ];

  fetch.mockResolvedValueOnce({
    ok: true,
    json: async () => mockNotes
  });

  render(<App />);

  await waitFor(() => {
    expect(screen.getByText('Test Note')).toBeInTheDocument();
    expect(screen.getByText('Test content')).toBeInTheDocument();
  });
});
