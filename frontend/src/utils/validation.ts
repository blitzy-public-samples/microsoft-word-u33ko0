/**
 * Check an email address and a password against Zod schemas, reporting only whether each
 * value satisfies its schema.
 *
 * Both exported functions build a schema and then call `safeParse`. `validateEmail` returns
 * the `.success` flag at L5 and `validatePassword` returns it at L14, so the message strings
 * configured at L10 and L12 never reach a caller.
 *
 * L1 imports `zod`, which `frontend/package.json:L6-L14` does not declare, so module
 * resolution fails and neither check runs as committed. Every other name here resolves: the
 * module carries no unused import and no undefined symbol.
 *
 * No module under `frontend/src` calls `validateEmail` or `validatePassword` today.
 *
 * Line locators: every `Lnn` reference below numbers the tree at commit
 * 06be74c7c88aa6bca652d465eaa00ad480a9e5c5, the frozen revision that precedes this documentation
 * pass. A bare `Lnn` points into this file, and a `path:Lnn` points into the named file. Current
 * HEAD numbers each documented file higher.
 *
 * @see frontend/src/utils/README.md for the register covering this directory.
 */

import { z } from 'zod';

/**
 * Report whether the given string is a valid email address.
 *
 * @param email - Candidate address checked against the `z.string().email()` schema built at L4.
 * @returns `true` when the schema accepts the value and `false` otherwise, read from the
 *   `safeParse(...).success` flag at L5.
 * @remarks The function returns only `.success`, so no failure detail reaches the caller. L1
 *   imports `zod`, which `frontend/package.json:L6-L14` does not declare, so the check cannot
 *   run as committed.
 */
export const validateEmail = (email: string): boolean => {
  const emailSchema = z.string().email();
  return emailSchema.safeParse(email).success;
};

/**
 * Report whether the given string satisfies the password policy.
 *
 * @param password - Candidate password checked against the schema built at L9-L13.
 * @returns `true` when the schema accepts the value and `false` otherwise, read from the
 *   `safeParse(...).success` flag at L14.
 * @remarks The policy holds six requirements. L10 sets a minimum of 8 characters. The anchored
 *   expression at L11-L13 demands at least one lowercase letter, one uppercase letter, one
 *   digit, and one character from `@$!%*?&`. That expression also confines the whole value to
 *   the class `[A-Za-z\d@$!%*?&]{8,}`, so a password holding any character outside
 *   `A-Za-z0-9@$!%*?&` fails even when it meets the other five. `Passw0rd@#` fails on the `#`
 *   alone. The function returns only `.success`, so the two message strings configured
 *   at L10 and L12 never reach a caller. L1 imports `zod`, which
 *   `frontend/package.json:L6-L14` does not declare, so the check cannot run as committed.
 */
export const validatePassword = (password: string): boolean => {
  const passwordSchema = z.string()
    .min(8, { message: "Password must be at least 8 characters long" })
    .regex(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/, {
      message: "Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character"
    });
  return passwordSchema.safeParse(password).success;
};