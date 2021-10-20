const { prompt } = require('inquirer');
const fs = require('fs');
const GifEncoder = require('gif-encoder');
const PNG = require('pngjs').PNG;

const hasPngExtension = str => str.substr(str.length-4) === ".png";
const removePngExtension = str => hasPngExtension(str) ? str.substr(0,str.length-4) : str;

const convertToGif = (props, name) => {
	const { directory, storage, framewidth, framerate, transparentcolor, quality } = props;
	const path = `${directory}/${name}.png`;
    fs.exists(path,exists=>{
        if(!exists){
            console.log("Could not open file " + path);
            return
        } 
    	fs.createReadStream(path)
        .pipe(new PNG())
        .on('parsed', function(){
        	const {data, width, height} = this;
        	// Create an object containing the rgb of transparentcolor
        	const transparentRGB = {
    			r:Number("0x"+transparentcolor.substr(0,2)),
    			g:Number("0x"+transparentcolor.substr(2,2)),
    			b:Number("0x"+transparentcolor.substr(4,2)),
        	};

        	// Create a 2D pixel array
     		let pixelmap = [];
     		for (let x = 0; x < width; x++) {
            	pixelmap.push([]);
          		for (let y = 0; y < height; y++) {
                    let idx = (width * y + x) << 2;
                    let r = data[idx];
                    let g = data[idx+1];
                    let b = data[idx+2];
                    let a = data[idx+3];

                    // Detect transparency and convert to our transparency color
                    if(a < 128){
                    	({r,g,b} = transparentRGB);
                    	a = 255;
                    }

                    pixelmap[x].push([r,g,b,a]);
                }
            }

            // Set gif dimensions
        	const fh = height;
        	const fw = framewidth === "" ? fh : Number(framewidth);

    		const file = require('fs').createWriteStream(`${storage}/${name}.gif`);
        	const gif = new GifEncoder(fw, fh, {
        	  highWaterMark: 5 * 1024 * 1024 // 5MB buffer
        	});
        	gif.setRepeat(0);
        	gif.setFrameRate(Number(framerate));
        	gif.setTransparent(Number("0x"+transparentcolor));
            gif.setQuality(Number(quality));

        	// Start writing gif
        	gif.pipe(file);
        	gif.writeHeader();
        	for(let i = 0; i*fw < width; i++){
        		// Create a 1D array of pixels for each frame
        		let pixels = [];
        		for (let y = 0; y < fh; y++) {
        		    for (let x = 0; x < fw; x++) {
        		    	pixels.push(pixelmap[(i*fw) + x][y][0]);
        		    	pixels.push(pixelmap[(i*fw) + x][y][1]);
        		    	pixels.push(pixelmap[(i*fw) + x][y][2]);
        		    	pixels.push(pixelmap[(i*fw) + x][y][3]);
        		    }
        		}
        		gif.addFrame(pixels);
        	}
        	gif.finish();
            console.log("Converted " + path);
        });
    });
        
	
}

const convertDir = props => {
	const { directory } = props;
	fs.readdir(directory, (err,data)=>{
		if (err){
			console.log(`Could not find directory ${directory}.`);
			return;
		};
		data.forEach(item=>{
			if(hasPngExtension(item)){
				convertToGif(props, removePngExtension(item));
			}
		});
	});
}

const questions = [
    {
        type : 'input',
        name : 'directory',
        default : "build/images",
        filter: dir => dir ? dir : ".",
        message : 'Enter folder directory. Press "enter" for auto:'
    },
    {
        type : 'input',
        name : 'name',
        message : 'Enter name (no extension). Leave blank to convert all:'
    },
    {
        type : 'input',
        name : 'storage',
        default : "build/gifs",
        filter: dir => dir ? dir : ".",
        message : 'Enter storage folder directory. Press "enter" for auto:'
    },
    {
        type : 'input',
        name : 'framerate',
        default : 30,
        message : 'Enter frames per second:'
    },
    {
        type : 'input',
        name : 'framewidth',
        message : 'Enter frame width. Leave blank for auto:'
    },
    {
        type : 'input',
        name : 'transparentcolor',
        default : "0000FF",
        message : 'Enter transparent color in hex:'
    },
    {
        type : 'input',
        name : 'quality',
        default : 10,
        message : 'Enter quality (1 = best; 20 = worst):'
    },
    {
        type : 'confirm',
        name : 'confirm',
        message : 'Proceed with conversion?'
    }
];

const startPrompt = () => {
	prompt(questions).then((answers) => {
		if(!answers.confirm){
			console.log("Conversion aborted.");
			return;
		}
		if(answers.name){
			convertToGif(answers, answers.name);
		} else {
			convertDir(answers);
		}
	})
	.catch(console.log);
}

startPrompt();
