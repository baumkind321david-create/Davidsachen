const podcastFeedParser = require("podcast-feed-parser");
const fs = require("fs").promises;
const path = require("path");
const crypto = require("crypto");

function buildCachePath(url) {
  const hash = crypto.createHash("sha256").update(url).digest("hex");
  return path.join("cache", `${hash}.json`);
}

function isPastDay(date) {
  return date.setHours(0, 0, 0, 0) - new Date().setHours(0, 0, 0, 0) < 0;
}

async function refreshFeed(url, cachePath) {
  const podcast = await podcastFeedParser.getPodcastFromURL(url);
  podcast.parseTimestamp = new Date();
  await fs.mkdir("cache", { recursive: true });
  await fs.writeFile(cachePath, JSON.stringify(podcast));
  return podcast;
}

async function exists(file) {
  try {
    await fs.access(file);
    return true;
  } catch {
    return false;
  }
}

async function parseFeed(url, callback) {
  const cachePath = buildCachePath(url);
  if (await exists(cachePath)) {
    let podcast = JSON.parse(await fs.readFile(cachePath));
    if (isPastDay(new Date(podcast.parseTimestamp))) {
      // Cache file older than 1 day --> serve from cache
      callback(await refreshFeed(url, cachePath));
    } else {
      // Cache file is fresh --> serve from cache
      callback(podcast);
    }
  } else {
    // No cache file --> refresh feed
    callback(await refreshFeed(url, cachePath));
  }
}

module.exports.parseFeed = parseFeed;