/**
 * Sentry Configuration for Next.js Frontend
 * Client-side and server-side error tracking
 */
import * as Sentry from "@sentry/nextjs";

const SENTRY_DSN = process.env.NEXT_PUBLIC_SENTRY_DSN;
const SENTRY_ENVIRONMENT = process.env.NEXT_PUBLIC_SENTRY_ENVIRONMENT || 'development';
const SENTRY_TRACES_SAMPLE_RATE = parseFloat(
  process.env.NEXT_PUBLIC_SENTRY_TRACES_SAMPLE_RATE || '0.1'
);
const SENTRY_REPLAYS_SESSION_SAMPLE_RATE = parseFloat(
  process.env.NEXT_PUBLIC_SENTRY_REPLAYS_SESSION_SAMPLE_RATE || '0.1'
);
const SENTRY_REPLAYS_ERROR_SAMPLE_RATE = parseFloat(
  process.env.NEXT_PUBLIC_SENTRY_REPLAYS_ERROR_SAMPLE_RATE || '1.0'
);

export function initSentry() {
  if (!SENTRY_DSN) {
    console.warn('Sentry DSN not configured, error tracking disabled');
    return;
  }

  Sentry.init({
    dsn: SENTRY_DSN,
    environment: SENTRY_ENVIRONMENT,

    // Performance Monitoring
    tracesSampleRate: SENTRY_TRACES_SAMPLE_RATE,

    // Session Replay
    replaysSessionSampleRate: SENTRY_REPLAYS_SESSION_SAMPLE_RATE,
    replaysOnErrorSampleRate: SENTRY_REPLAYS_ERROR_SAMPLE_RATE,

    // Privacy settings
    sendDefaultPii: false,

    // Integrations
    integrations: [
      Sentry.replayIntegration({
        maskAllText: true,
        blockAllMedia: true,
      }),
    ],

    // Release tracking
    release: process.env.NEXT_PUBLIC_APP_VERSION || '1.0.0',

    // Error filtering
    beforeSend(event, hint) {
      return filterErrors(event, hint);
    },

    // Ignore certain errors
    ignoreErrors: [
      // Browser extensions
      'top.GLOBALS',
      'chrome-extension://',
      'moz-extension://',

      // Network errors that are not actionable
      'NetworkError',
      'Network request failed',
      'Failed to fetch',

      // Cancelled requests
      'AbortError',
      'Request aborted',

      // Common non-critical errors
      'ResizeObserver loop limit exceeded',
      'Non-Error promise rejection captured',
    ],

    // Denylist for URLs to ignore
    denyUrls: [
      // Browser extensions
      /extensions\//i,
      /^chrome:\/\//i,
      /^moz-extension:\/\//i,

      // Analytics and ads
      /google-analytics\.com/i,
      /googletagmanager\.com/i,
    ],
  });

  console.info('Sentry initialized', {
    environment: SENTRY_ENVIRONMENT,
    tracesSampleRate: SENTRY_TRACES_SAMPLE_RATE,
  });
}

function filterErrors(event: Sentry.Event, hint: Sentry.EventHint): Sentry.Event | null {
  // Don't send validation errors or client errors (4xx)
  if (hint.originalException) {
    const error = hint.originalException as any;

    // Filter axios/fetch errors with 4xx status codes
    if (error.response?.status && error.response.status < 500) {
      return null;
    }
  }

  // Sanitize sensitive data
  if (event.request) {
    const request = event.request;

    // Remove sensitive headers
    if (request.headers) {
      const sensitiveHeaders = ['authorization', 'cookie', 'x-api-key'];
      sensitiveHeaders.forEach(header => {
        if (request.headers && header in request.headers) {
          request.headers[header] = '[Filtered]';
        }
      });
    }

    // Remove sensitive query params
    if (request.query_string) {
      const sensitiveParams = ['token', 'password', 'secret', 'api_key'];
      const queryString = request.query_string.toLowerCase();
      if (sensitiveParams.some(param => queryString.includes(param))) {
        request.query_string = '[Filtered]';
      }
    }
  }

  return event;
}

/**
 * Capture exception with additional context
 */
export function captureException(error: Error, context?: Record<string, any>) {
  if (context) {
    Sentry.withScope(scope => {
      Object.entries(context).forEach(([key, value]) => {
        scope.setContext(key, value);
      });
      Sentry.captureException(error);
    });
  } else {
    Sentry.captureException(error);
  }
}

/**
 * Capture message with additional context
 */
export function captureMessage(
  message: string,
  level: Sentry.SeverityLevel = 'info',
  context?: Record<string, any>
) {
  if (context) {
    Sentry.withScope(scope => {
      Object.entries(context).forEach(([key, value]) => {
        scope.setContext(key, value);
      });
      Sentry.captureMessage(message, level);
    });
  } else {
    Sentry.captureMessage(message, level);
  }
}

/**
 * Set user context for error tracking
 */
export function setUserContext(userId: string, email?: string, username?: string) {
  Sentry.setUser({
    id: userId,
    email,
    username,
  });
}

/**
 * Clear user context (e.g., on logout)
 */
export function clearUserContext() {
  Sentry.setUser(null);
}

/**
 * Add breadcrumb for debugging
 */
export function addBreadcrumb(
  message: string,
  category?: string,
  level?: Sentry.SeverityLevel,
  data?: Record<string, any>
) {
  Sentry.addBreadcrumb({
    message,
    category,
    level,
    data,
  });
}
