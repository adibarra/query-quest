/**
 * @author: adibarra (Alec Ibarra)
 * @description: Composable for providing utility functions
 */

const { width, height } = useWindowSize()

/**
 * A computed boolean indicating whether the current device is a mobile device screen size.
 * @returns True if the device is a mobile device, false otherwise.
 */
export const isMobile = computed<boolean>(() => {
  return width.value < 640 || height.value < 640
})

/**
 * A computed boolean indicating whether the current device is running on a mobile OS.
 * @returns True if the device is a mobile OS, false otherwise.
 */
export const isMobileOS = computed<boolean>(() => {
  return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)
})

/**
 * Removes all properties with falsy values from an object.
 * @param obj - The object to remove empty properties from.
 * @returns The object with empty properties removed.
 */
export function removeEmpty(obj: any): any {
  Object.keys(obj).forEach(key => !obj[key] && delete obj[key])
  return obj
}

/**
 * Clamps a number between a minimum and maximum value.
 * @param num - The number to clamp.
 * @param min - The minimum value to clamp the number to.
 * @param max - The maximum value to clamp the number to.
 * @returns The clamped number.
 */
export function clamp(num: number, min: number, max: number): number {
  return Math.min(Math.max(num, min), max)
}

/**
 * Expands a template string by replacing placeholders with values from a map of functions.
 * @param str - The template string with placeholders.
 * @param map - Object mapping placeholders to functions.
 * @returns The expanded string.
 */
export function expandTemplate(str: string, map: Record<string, () => string>): string {
  return str.replaceAll(/\{(.*?)\}/g, (match, key) => (map[key] ? map[key]() : match))
}
